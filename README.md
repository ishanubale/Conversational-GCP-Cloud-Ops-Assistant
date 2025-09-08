🤖 CloudOps AI Assistant (LangChain + Vertex AI) 
   This project is converstion AI CloudOps Assistant built using LangChain, Google Cloud Vertex AI (Gemini models + Embeddings), and Streamlit for userinterface. It is designed to troubleshoot GCP issues, provide step-by-step guidance, and leverage Retrieval-Augmented Generation (RAG) for real-time documentation support.

🚀 Features 
- LLM Integration (Vertex AI) → Uses gemini-2.5-flash-lite for low-latency troubleshooting. 
- RAG   (Retrieval-Augmented Generation) → Fetches and indexes GCP documentation for context-aware answers. 
- FAISS Vector Store → Stores embeddings for fast document retrieval. 
- Secure Config → Environment variables & service account authentication. 
- Streamlit Frontend → Simple chat UI for back-and-forth conversations.

📂 Project Structure 
 ├── agent.py # Main agent logic (LLM + RAG) 
 ├── UI.py # Streamlit chat UI 
 ├── ragInit.py # RAG initialization (load docs, create embeddings) 
 ├── .env # Environment variables 
 ├── requirements.txt # Python dependencies 
 ├── .gitignore # Git ignore rules 
 └── gcp_faiss_index # (Ignored) Vector embeddings storage created using script

 Steps for setup: 
 1. Clone the Repository 
 2. Create Virtual Environment 
 3. Install Dependencies pip install -r requirements.txt 
 4. Setup Google Cloud Authentication Enable Vertex AI API in your GCP project. Create a Service Account with     Vertex AI User and Storage Object Viewer roles. Download the JSON key and store it in your project (e.g., serviceKey.json). 
 5.Configure Environment Variables GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_REGION.

 Steps to run: 
 1. Initialize RAG = cmd-> python ragInit.py 
 2. Run Agent (CLI Test) = cmd -> python agent.py 
 3. Start Chat UI = cmd -> streamlit run UI.py
