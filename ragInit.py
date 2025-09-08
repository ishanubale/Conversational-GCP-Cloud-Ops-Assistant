from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAIEmbeddings
from dotenv import load_dotenv
import vertexai
import os

load_dotenv()

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_REGION"),
)

# Pick a few GCP docs to showcase
URLS = [
    "https://cloud.google.com/run/docs/overview",
    "https://cloud.google.com/logging/docs/overview",
    "https://cloud.google.com/compute/docs/troubleshooting",
]

def build_vectorstore():
    print("📥 Loading Google Cloud documentation...")
    loader = WebBaseLoader(URLS)
    docs = loader.load()

    print("🔀 Splitting docs into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    print("🔎 Creating embeddings with Vertex AI...")
    embeddings = VertexAIEmbeddings(model_name="text-embedding-004")

    print("💾 Storing in FAISS vector database...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Save for reuse
    vectorstore.save_local("gcp_faiss_index")
    print("✅ Vectorstore saved locally: gcp_faiss_index/")

if __name__ == "__main__":
    build_vectorstore()
