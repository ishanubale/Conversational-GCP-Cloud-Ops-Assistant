import os
from dotenv import load_dotenv
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAIEmbeddings


# Load environment variables from .env file
load_dotenv()

# Get environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
region = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not project_id:
    raise ValueError("Missing GOOGLE_CLOUD_PROJECT in .env")
if not credentials_path:
    raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS in .env")
if not region:
    raise ValueError("Missing region in .env")

# Initialize the Vertex AI LLM
llm = ChatVertexAI(
    model_name="gemini-2.5-flash-lite", #LLM model used under vertexAI
    temperature=0.3,
    location=region,
    project=project_id
)

# Load the same embedding model used during FAISS index creation
embedding_model = VertexAIEmbeddings(model_name="text-embedding-004")

# Load FAISS index instead of rebuilding
def load_vectorstore():
    return FAISS.load_local(
        "gcp_faiss_index",   #folder where you stored vector indexing data 
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )

vectorstore = load_vectorstore()

# Setup retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Custom system prompt
prompt = ChatPromptTemplate.from_template("""
You are a CloudOps AI Assistant
You specialize in **troubleshooting GCP issues** and 
giving **clear, step-by-step answers which a 10 year old can understand easily**.

Guidelines:
- Always read the user’s query carefully.extract all the context data and ask back if something is missing.
- If the query is about GCP services, check retrieved docs before answering.
- Use the provided context to ground your answers.
- Give short, actionable answers. 
- If unsure, say: "I don’t have enough data, please provide logs."
- Dont ask for service keys  or any api keys explicitly not ask any personal client related data which is not needed.

Context:
{context}

User question:
{question}
                                          
""")


# Build Retrieval-QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

def run_agent(query: str) -> str:
    """Handles user query via Vertex AI agent + RAG."""
    try:
        response = qa_chain.run(query)
        return response
    except Exception as e:
        return f"⚠️ Error: {e}"

# Example test
if __name__ == "__main__":
    print(run_agent("How do I troubleshoot Cloud Run 502 errors?"))
