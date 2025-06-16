# ingest/test_retriever.py

from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# Step 1: Load embeddings (must match what was used during ingestion)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Step 2: Load Chroma vector store
db = Chroma(persist_directory="./vector_store", embedding_function=embedding_model)

# Step 3: Ask your query
query = "What is a inheritance in Java ?"

# Step 4: Retrieve relevant chunks
results = db.similarity_search(query, k=3)

# Step 5: Print the top 3 matching chunks
print("\n🔍 Top Matching Chunks:\n" + "-" * 40)
for i, doc in enumerate(results, 1):
    print(f"[{i}] {doc.page_content[:500]}...\n")
