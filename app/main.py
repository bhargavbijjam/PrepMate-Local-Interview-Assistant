import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.llms import Ollama
from ollama_stream import stream_response_to_streamlit

llm = Ollama(model="phi3")
llm.invoke("Hello")  # Optional warm-up

@st.cache_resource
def load_llm():
    return Ollama(model="phi3")

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource
def load_vector_db():
    embeddings = load_embeddings()
    return Chroma(persist_directory="./vector_store", embedding_function=embeddings)

def truncate_context(context, max_tokens=700):
    max_chars = max_tokens * 4
    return context[:max_chars]

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="PrepMate: Local Interview Assistant")
st.title("📚 PrepMate: Local Interview Assistant")
st.markdown("Ask anything from your local study materials!")

query = st.text_input("🔎 Enter your question")

if query:
    with st.spinner("🔍 Searching..."):
        db = load_vector_db()
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""Answer the question below using the given context. 
If the answer isn't in the context, reply with 'I don't know.'

### Context:
{truncate_context(context)}

### Question:
{query}

### Answer:"""

    st.success("✅ Answer generated:")
    stream_response_to_streamlit(prompt)

    with st.expander("📄 Top retrieved chunks"):
        for i, doc in enumerate(docs, 1):
            st.markdown(f"**[{i}]** {doc.page_content[:500]}...")
