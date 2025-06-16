# PrepMate: Local Interview Assistant 🤖

**PrepMate** is a fully local, privacy-first AI assistant that helps students prepare for technical interviews using their own study materials. It combines RAG (Retrieval Augmented Generation), HuggingFace embeddings, ChromaDB, and local LLMs like Phi-3 via Ollama.

---

## 🚀 Features

- ✅ Ingest and index personal notes (PDF, text)
- 🔍 Semantic search using HuggingFace embeddings
- 🧠 Contextual answers using local LLM (Phi-3)
- 🔒 Fully offline and private
- 💻 Fast response via optimized local retrieval pipeline

---

## 🧠 Architecture

User Query
↓
Chroma Vector Search ← (Docs → Text Splitter → Embeddings)
↓
Retrieved Chunks + Query → Prompt
↓
Phi-3 LLM (via Ollama or HF) → Answer
↓
Displayed via Streamlit UI

---

## 🧰 Tech Stack

- 🦜 LangChain
- 🤗 Sentence Transformers (MiniLM)
- 📦 Chroma Vector Store
- 🔁 Ollama + Phi-3 (or HuggingFace)
- 🎛️ Streamlit (frontend)
- 🗂️ Python, Faiss, dotenv, etc.

---

## ⚙️ Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/bhargavbijjam/PrepMate-Local-Interview-Assistant.git
cd PrepMate-Local-Interview-Assistant
```
### 2. Create Virtual Env & Install Deps
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
### 3. Run the App
streamlit run app/main.py
