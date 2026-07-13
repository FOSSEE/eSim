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

def _get_collection():
    """Create a thread-local client and collection to avoid SQLite multi-threading crashes."""
    client = chromadb.PersistentClient(path=db_path)
    return client.get_or_create_collection(name="esim_manuals")

# ==================== INGESTION ====================
def read_paragraphs(file_path: str):
    """Lazily read a file paragraph-by-paragraph to avoid high memory usage."""
    with open(file_path, "r", encoding="utf-8") as f:
        paragraph = []
        for line in f:
            if line.strip() == "":
                if paragraph:
                    yield "".join(paragraph)
                    paragraph = []
            else:
                paragraph.append(line)
        if paragraph:
            yield "".join(paragraph)

# ==================== INGESTION ====================
def ingest_pdfs(manuals_directory: str) -> None:
    """
    Read the single master text file and index it.
    Call this once from src/ingest.py.
    """
    if not os.path.exists(manuals_directory):
        print("Directory not found.")
        return

    # Look for .txt files only
    files = [f for f in os.listdir(manuals_directory) if f.lower().endswith(".txt")]
    
    if not files:
        print("❌ No .txt files found to ingest!")
        return

    all_documents, all_embeddings, all_metadatas, all_ids = [], [], [], []
    chunk_counter = 0

    for filename in files:
        path = os.path.join(manuals_directory, filename)
        print(f"\n📄 Processing Master File: {filename}")

        try:
            for paragraph in read_paragraphs(path):
                section = paragraph.strip()
                if len(section) < 50:
                    continue
                
                # Further split large sections by double newlines if needed
                sub_chunks = [c.strip() for c in section.split("\n\n") if len(c) > 50]
                
                for chunk in sub_chunks:
                    embed = get_embedding(chunk)
                    if embed:
                        all_documents.append(chunk)
                        all_embeddings.append(embed)
                        all_metadatas.append({"source": filename, "type": "master_ref"})
                        all_ids.append(f"{filename}_{chunk_counter}")
                        chunk_counter += 1

        except Exception as e:
            print(f" ❌ Failed to process {filename}: {e}")

    if all_documents:
        # Clear existing DB only after successfully generating all embeddings
        print("Clearing old database...")
        try:
            client = chromadb.PersistentClient(path=db_path)
            client.delete_collection("esim_manuals")
            collection = client.get_or_create_collection(name="esim_manuals")
        except Exception as e:
            print(f"Warning clearing DB: {e}")
            collection = _get_collection()

        collection.add(
            documents=all_documents,
            embeddings=all_embeddings,
            metadatas=all_metadatas,
            ids=all_ids,
        )
        print(f" ✅ Successfully indexed {len(all_documents)} total chunks.")
    else:
        print(" ⚠️ No valid chunks found to index. Database was not cleared.")


# ==================== SEARCH ====================

# Relevance threshold: ChromaDB returns distances (L2 or cosine).
# Lower distance = more similar. Filter out chunks with distance > threshold.
# ChromaDB distances for nomic-embed-text embeddings are typically
# in the hundreds. Results above 500 are considered insufficiently
# relevant and are filtered out.
RELEVANCE_THRESHOLD = float(
    os.environ.get("ESIM_RAG_RELEVANCE_THRESHOLD", "500")
)
RELEVANCE_THRESHOLD = float(os.environ.get("ESIM_RAG_RELEVANCE_THRESHOLD", "500"))


def search_knowledge(query: str, n_results: int = 4) -> str:
    """
    Semantic search with relevance threshold to reduce hallucination.
    Filters out chunks with distance > RELEVANCE_THRESHOLD.
    """
    try:
        query_embed = get_embedding(query)
        if not query_embed:
            return ""

        collection = _get_collection()
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
