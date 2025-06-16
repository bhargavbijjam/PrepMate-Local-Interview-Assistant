from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import requests

retriever = Chroma(persist_directory="vector_store", embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")).as_retriever()

query = "What is inheritance in Java?"
docs = retriever.get_relevant_documents(query)
context = "\n\n".join(doc.page_content for doc in docs[:3])
prompt = f"Answer the following question using the context:\n\n{context}\n\nQuestion: {query}"

response = requests.post("http://localhost:11434/api/generate", json={"model": "phi3", "prompt": prompt, "stream": False})
print(response.json()["response"])
