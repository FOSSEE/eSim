import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from chatbot.knowledge_base import ingest_pdfs

pdf_folder = os.path.join(current_dir, "manuals")

if not os.path.exists(pdf_folder):
    print(f"Error: Folder not found: {pdf_folder}")
    sys.exit(1)

print(f"📂 Scanning folder: {pdf_folder}")

files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf') or f.endswith('.txt')]
print(f"📄 Found {len(files)} Document(s): {files}")

if not files:
    print("No PDFs or Text files found to ingest.")
    sys.exit()

print("\n🚀 Starting Ingestion... (Press Ctrl+C to stop)")
try:
    ingest_pdfs(pdf_folder)
    print("\n✅ Ingestion Complete!")
except KeyboardInterrupt:
    print("\n⚠️ Ingestion stopped by user.")
except Exception as e:
    print(f"\n❌ Error: {e}")
