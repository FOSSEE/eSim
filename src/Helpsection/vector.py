from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Load the CSV data
df = pd.read_csv("resources/esim_help.csv")

# Initialize embeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Database location
db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    print("[Vector] Creating new vector database...")
    documents = []
    ids = []
    
    for i, row in df.iterrows():
        # Handle NaN values by converting to empty strings
        command = str(row['command']) if pd.notna(row['command']) else ""
        category = str(row['category']) if pd.notna(row['category']) else ""
        subcategory = str(row['subcategory']) if pd.notna(row['subcategory']) else ""
        syntax = str(row['syntax']) if pd.notna(row['syntax']) else ""
        description = str(row['description']) if pd.notna(row['description']) else ""
        example = str(row['example']) if pd.notna(row['example']) else ""
        parameters = str(row['parameters']) if pd.notna(row['parameters']) else ""
        notes = str(row['notes']) if pd.notna(row['notes']) else ""
        use_case = str(row['use_case']) if pd.notna(row['use_case']) else ""
        related_commands = str(row['related_commands']) if pd.notna(row['related_commands']) else ""
        
        # Create focused content for better semantic search
        page_content_parts = []
        
        if command:
            page_content_parts.append(f"Command: {command}")
        if category:
            page_content_parts.append(f"Category: {category}")
        if subcategory:
            page_content_parts.append(f"Subcategory: {subcategory}")
        if description:
            page_content_parts.append(f"Description: {description}")
        if syntax:
            page_content_parts.append(f"Syntax: {syntax}")
        if example:
            page_content_parts.append(f"Example: {example}")
        if use_case:
            page_content_parts.append(f"Use case: {use_case}")
        if parameters:
            page_content_parts.append(f"Parameters: {parameters}")
        if notes:
            page_content_parts.append(f"Notes: {notes}")
        if related_commands:
            page_content_parts.append(f"Related commands: {related_commands}")
        
        page_content = ". ".join(page_content_parts)
        
        # Comprehensive metadata
        metadata = {
            "command": command,
            "category": category,
            "subcategory": subcategory,
            "syntax": syntax,
            "description": description,
            "example": example,
            "parameters": parameters,
            "notes": notes,
            "use_case": use_case,
            "related_commands": related_commands,
            "row_index": i
        }
        
        document = Document(page_content=page_content, metadata=metadata)
        doc_id = f"{command}_{i}" if command else f"doc_{i}"
        
        ids.append(doc_id)
        documents.append(document)
    
    print(f"[Vector] Created {len(documents)} documents")

# Initialize vector store
vector_store = Chroma(
    collection_name="ngspice_commands_db",
    embedding_function=embeddings,
    persist_directory=db_location,
)

if add_documents:
    print("[Vector] Adding documents to vector store...")
    # Add documents in batches to avoid memory issues
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        vector_store.add_documents(batch_docs, ids=batch_ids)
        print(f"[Vector] Added batch {i//batch_size + 1}/{(len(documents) + batch_size - 1)//batch_size}")
    
    print("[Vector] Persisting vector store...")
    vector_store.persist()
    print("[Vector] Vector database created successfully!")
else:
    print("[Vector] Loading existing vector database...")

# Create retriever with optimized search parameters
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5  # Return top 5 most relevant documents
    }
)

print("[Vector] Vector database and retriever initialized successfully!")