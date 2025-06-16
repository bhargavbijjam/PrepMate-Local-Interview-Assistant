# ingest/ingest_docs.py

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

import os
import glob

DOCS_PATH = r"C:\Users\bharg\OneDrive\Desktop\placement_interview_preparation_assistant\docs"
VECTOR_STORE_PATH = r"C:\Users\bharg\OneDrive\Desktop\placement_interview_preparation_assistant\vector_store"

# Load documents (PDFs and .txt)
print("[📥] Loading documents...")
documents = []
for file in glob.glob(os.path.join(DOCS_PATH, "*")):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(file)
    elif file.endswith(".txt"):
        loader = TextLoader(file, encoding="utf-8")
    else:
        continue
    documents.extend(loader.load())

# Split documents
print(f"[✂️] Splitting {len(documents)} documents into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=30)
chunks = splitter.split_documents(documents)

# Embed with local HuggingFace model
print("[🧠] Generating embeddings locally using HuggingFace...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Save to Chroma DB
print(f"[💾] Storing embeddings in Chroma DB at: {VECTOR_STORE_PATH}")
vectordb = Chroma.from_documents(documents=chunks, embedding=embedding_model, persist_directory=VECTOR_STORE_PATH)
vectordb.persist()

print("[✅] All embeddings stored successfully!")
