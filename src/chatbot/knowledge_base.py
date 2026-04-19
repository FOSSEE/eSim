import os
import chromadb
from .ollama_runner import get_embedding

# ==================== DATABASE SETUP ====================

def _default_db_path() -> str:
    xdg_data_home = os.environ.get("XDG_DATA_HOME", "").strip()
    if not xdg_data_home:
        xdg_data_home = os.path.join(os.path.expanduser("~"), ".local", "share")
    return os.path.join(xdg_data_home, "esim-copilot", "chroma")

db_path = os.environ.get("ESIM_COPILOT_DB_PATH", "").strip() or _default_db_path()
os.makedirs(db_path, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=db_path)

collection = chroma_client.get_or_create_collection(name="esim_manuals")

# ==================== INGESTION ====================
def ingest_pdfs(manuals_directory: str) -> None:
    """
    Read the single master text file and index it.
    Call this once from src/ingest.py.
    """
    if not os.path.exists(manuals_directory):
        print("Directory not found.")
        return

    # Clear existing DB to ensure no duplicates from old files
    print("Clearing old database...")
    try:
        chroma_client.delete_collection("esim_manuals")
        global collection
        collection = chroma_client.get_or_create_collection(name="esim_manuals")
    except Exception as e:
        print(f"Warning clearing DB: {e}")

    # Look for .txt files only
    files = [f for f in os.listdir(manuals_directory) if f.lower().endswith(".txt")]
    
    if not files:
        print("❌ No .txt files found to ingest!")
        return

    for filename in files:
        path = os.path.join(manuals_directory, filename)
        print(f"\n📄 Processing Master File: {filename}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            raw_sections = text.split("\n\n")
            
            documents, embeddings, metadatas, ids = [], [], [], []
            
            chunk_counter = 0
            for section in raw_sections:
                section = section.strip()
                if len(section) < 50:
                    continue
                
                # Further split large sections by double newlines if needed
                sub_chunks = [c.strip() for c in section.split("\n\n") if len(c) > 50]
                
                for chunk in sub_chunks:
                    embed = get_embedding(chunk)
                    if embed:
                        documents.append(chunk)
                        embeddings.append(embed)
                        metadatas.append({"source": filename, "type": "master_ref"})
                        ids.append(f"{filename}_{chunk_counter}")
                        chunk_counter += 1

            if documents:
                collection.add(
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    ids=ids,
                )
                print(f" ✅ Indexed {len(documents)} chunks from {filename}")
            else:
                print(f" ⚠️ No valid chunks found in {filename}")

        except Exception as e:
            print(f" ❌ Failed to process {filename}: {e}")


# ==================== SEARCH ====================

# Relevance threshold: ChromaDB returns distances (L2 or cosine).
# Lower distance = more similar. Filter out chunks with distance > threshold.
RELEVANCE_THRESHOLD = float(os.environ.get("ESIM_RAG_RELEVANCE_THRESHOLD", "1.0"))


def search_knowledge(query: str, n_results: int = 4) -> str:
    """
    Semantic search with relevance threshold to reduce hallucination.
    Filters out chunks with distance > RELEVANCE_THRESHOLD.
    """
    try:
        query_embed = get_embedding(query)
        if not query_embed:
            return ""

        results = collection.query(
            query_embeddings=[query_embed],
            n_results=n_results,
            include=["documents", "distances"],
        )

        docs_list = results.get("documents", [[]])
        distances_list = results.get("distances", [[]])

        if not docs_list or not docs_list[0]:
            return ""

        docs = docs_list[0]
        distances = distances_list[0] if distances_list else []

        # Filter by relevance threshold (lower distance = more similar)
        if distances and len(distances) == len(docs):
            filtered = [
                (doc, d) for doc, d in zip(docs, distances)
                if d <= RELEVANCE_THRESHOLD
            ]
            if filtered:
                selected_chunks = [doc for doc, _ in filtered]
            else:
                return ""
        else:
            selected_chunks = docs

        context_text = "\n\n...\n\n".join(selected_chunks)
        if len(context_text) > 3500:
            context_text = context_text[:3500]

        header = "=== ESIM OFFICIAL DOCUMENTATION ===\n"
        return f"{header}{context_text}\n===================================\n"

    except Exception as e:
        print(f"RAG Error: {e}")
        return ""
