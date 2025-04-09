from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import pipeline
import tempfile
from PyPDF2 import PdfReader

# ✅ Updated embedding (non-deprecated)
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = None

def ingest_document(file_content):
    global vector_store

    # Save uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name

    # Extract text from PDF
    reader = PdfReader(tmp_path)
    raw_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(raw_text)

    # Vectorize and add to FAISS
    if vector_store is None:
        vector_store = FAISS.from_texts(chunks, embedding=embedding_model)
    else:
        new_store = FAISS.from_texts(chunks, embedding=embedding_model)
        vector_store.merge_from(new_store)

    return f"Ingested {len(chunks)} text chunks."

# ✅ Load lightweight text generator (gpt2)
llm_pipeline = pipeline("text-generation", model="gpt2", max_new_tokens=100)
llm = HuggingFacePipeline(pipeline=llm_pipeline)

def query_rag(query: str) -> str:
    if vector_store is None:
        return "No documents ingested yet."
    
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=vector_store.as_retriever())
    return qa.run(query)
