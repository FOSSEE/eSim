import os
import chromadb
from .ollama_runner import get_embedding

# ==================== DATABASE SETUP ====================

# Persistent DB directory (relative to this file)
db_path = os.path.join(os.path.dirname(__file__), "esim_knowledge_db")
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

def search_knowledge(query: str, n_results: int = 4) -> str:
    """
    Simple semantic search against the single master knowledge file.
    """
    try:
        # Generate embedding for the user's question
        query_embed = get_embedding(query)
        if not query_embed:
            return ""

        # Query the database
        results = collection.query(
            query_embeddings=[query_embed],
            n_results=n_results,
        )

        docs_list = results.get("documents", [])
        
        if not docs_list or not docs_list[0]:
            print("DEBUG: No relevant info found.")
            return ""

        selected_chunks = docs_list[0]
        context_text = "\n\n...\n\n".join(selected_chunks)

        if len(context_text) > 3500:
            context_text = context_text[:3500]

        header = "=== ESIM OFFICIAL DOCUMENTATION ===\n"
        return f"{header}{context_text}\n===================================\n"

    except Exception as e:
        print(f"RAG Error: {e}")
        return ""
