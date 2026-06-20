# 📄 AWS Customer Agreement - RAG Question Answering System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-orange)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A production-ready **Retrieval-Augmented Generation (RAG)** system that answers questions about the AWS Customer Agreement document, with a FastAPI backend, SQL-based usage analytics, and a Streamlit frontend dashboard.

---

## 🚀 Features

- **🤖 RAG Pipeline**: Chunks PDF documents, generates embeddings, stores in ChromaDB, and retrieves relevant context for LLM generation
- **🔒 Hallucination Prevention**: Custom system prompt ensures the model only answers based on provided context
- **📊 SQL Analytics**: Logs all queries with response times, sources, and tracks most frequent questions
- **⚡ FastAPI Backend**: RESTful API with Swagger documentation, Pydantic validation, and error handling
- **🎨 Streamlit Dashboard**: User-friendly chat interface with real-time analytics view
- **📝 Source Attribution**: Every answer includes citations to the exact document chunks used

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                         │
│                    (Streamlit Dashboard)                       │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP Requests
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FASTAPI BACKEND                         │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐  │
│  │  /ingest    │  │   /ask      │  │    /analytics         │  │
│  │  (PDF Load) │  │  (RAG Q&A)  │  │  (SQL Aggregations)   │  │
│  └─────────────┘  └─────────────┘  └──────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐
│   VECTOR STORE  │  │   SQLite DB     │  │    OPENAI API       │
│   (ChromaDB)    │  │  (Query Logs)   │  │  (Embeddings + LLM) │
└─────────────────┘  └─────────────────┘  └─────────────────────┘
```

### Data Flow

1. **Ingestion Phase**: PDF → Text Extraction → Chunking → Embeddings → Vector Store
2. **Query Phase**: User Question → Retrieve Top-k Chunks → Build Prompt → LLM Generation → Response + Sources
3. **Logging Phase**: Every query is logged with metadata (timestamp, response time, found answer status)
4. **Analytics Phase**: SQL queries aggregate logs for dashboard visualization

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Language** | Python 3.9+ | Core programming language |
| **PDF Processing** | PyPDF2 / LangChain PDF Loader | Extract text from PDF |
| **Text Chunking** | RecursiveCharacterTextSplitter | Split document into manageable chunks |
| **Embeddings** | OpenAI `text-embedding-3-large` | Generate vector representations |
| **Vector Store** | ChromaDB | Store and retrieve embeddings |
| **LLM** | OpenAI `gpt-4.1-nano` | Generate answers from context |
| **Backend** | FastAPI | RESTful API server |
| **Validation** | Pydantic | Request/response validation |
| **Database** | SQLite | Query logging and analytics |
| **Frontend** | Streamlit | Interactive dashboard |
| **HTTP Client** | Requests | Frontend-to-backend communication |
| **Environment** | python-dotenv | Manage environment variables |

---

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key (or use Ollama/HuggingFace for free alternatives)
- Git (for cloning)

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/rag-aws-agreement.git
cd rag-aws-agreement
```

### 2. Create and Activate Virtual Environment

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**⚠️ Important**: Never commit your `.env` file to version control.

### 5. Place the PDF Document

Ensure the AWS Customer Agreement PDF is in the `data/` directory:

```
data/
└── AWS Customer Agreement.pdf
```

---

## 🚀 Running the Application

### Option A: Run with Script (Recommended)

#### Windows (`run.bat`):
```batch
@echo off
echo Starting FastAPI backend...
start cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout 3

echo Starting Streamlit frontend...
start cmd /k "streamlit run frontend/streamlit_app.py"
```

#### macOS/Linux (`run.sh`):
```bash
#!/bin/bash
echo "Starting FastAPI backend..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

sleep 3

echo "Starting Streamlit frontend..."
streamlit run frontend/streamlit_app.py
```

Make the script executable (Linux/macOS):
```bash
chmod +x run.sh
./run.sh
```

---

### Option B: Run Manually (Two Terminals)

#### Terminal 1 - FastAPI Backend:
```bash
# First, ingest the document (one-time setup)
curl -X POST http://localhost:8000/ingest

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Streamlit Frontend:
```bash
streamlit run frontend/streamlit_app.py
```

---

## 🧪 Testing the API

### 1. Swagger UI Documentation

Open your browser and navigate to:
```
http://localhost:8000/docs
```

You'll see interactive API documentation where you can test all endpoints.

### 2. Test with curl

#### Ingest Document:
```bash
curl -X POST http://localhost:8000/ingest
```

#### Ask a Question:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the payment terms?", "top_k": 3}'
```

#### Get Analytics:
```bash
curl http://localhost:8000/analytics
```

#### Health Check:
```bash
curl http://localhost:8000/health
```

### 3. Populate Database with Test Queries

Run the helper script to generate 30+ test queries:

```bash
python populate_logs.py
```

---

## 🎨 Frontend Dashboard

The Streamlit dashboard provides:

### Chat Interface (Left Panel)
- Ask questions about the AWS agreement
- View answers with source attribution
- See answer status (found/not found)
- Expand sources to view exact chunks used

### Analytics Dashboard (Right Panel)
- **Total Queries**: Count of all queries made
- **No Answer Rate**: Percentage of questions without answers
- **Average Response Time**: Mean latency in milliseconds
- **Most Frequent Questions**: Table of popular queries

---

## 📁 Project Structure

```
rag-aws-agreement/
├── src/                          # Core RAG modules
│   ├── __init__.py
│   ├── config.py                 # Configuration & system prompt
│   ├── pdf_loader.py             # PDF loading
│   ├── chunker.py                # Document chunking
│   ├── embeddings.py             # Embedding generation
│   ├── vector_store.py           # ChromaDB operations
│   ├── rag_pipeline.py           # Main RAG logic
│   └── schemas.py                # Pydantic models
│                       
│   ├── __init__.py
│   ├── main.py                   # API endpoints
│   └── database.py               # SQLite operations
│
├── frontend/                     # Streamlit UI
│   └── streamlit_app.py          # Dashboard
│                    
│   └── populate_logs.py          # Generate test queries
│
├── data/                         # Data files
│   └── AWS Customer Agreement.pdf
│
├── logs/                         # Database files
│   └── rag.db                    # SQLite database (auto-created)
│
├── vector_db/                    # ChromaDB storage (auto-created)
│
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (ignored)
├── .gitignore                    # Git ignore file
└── README.md                     # Project documentation
```

---

## 🧠 Key Design Decisions

### 1. Chunking Strategy
- **Chunk Size**: 500 tokens
- **Overlap**: 100 tokens
- **Justification**: Legal documents often span multiple paragraphs. 500 tokens captures sufficient context while the overlap prevents cutting critical information mid-sentence.

### 2. Top-k Selection
- **Value**: 3
- **Justification**: Using 3 chunks provides enough context without overwhelming the LLM. This balances retrieval relevance with context window limits.

### 3. System Prompt Engineering
- **Strict Grounding**: Model only answers from provided context
- **Hallucination Prevention**: Explicit fallback response for out-of-scope queries
- **Source Attribution**: Mandatory citation of source chunks
- **Justification**: Crucial for legal document Q&A where accuracy and compliance are paramount.

### 4. Model Choice
- **LLM**: OpenAI GPT-4.1-nano (or GPT-3.5-turbo)
- **Embeddings**: OpenAI text-embedding-3-large
- **Justification**: Production-grade models with reliable performance and reasonable cost.

### 5. Database Choice
- **Database**: SQLite
- **Justification**: Lightweight, zero-configuration, perfect for local development and meets all analytics requirements.

### 6. Vector Store
- **Technology**: ChromaDB
- **Justification**: Easy setup, persistent storage, and excellent Python integration.

---

## 📊 SQL Schema

### Query Logs Table

```sql
CREATE TABLE IF NOT EXISTS query_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    sources TEXT NOT NULL,          -- JSON list of source chunks
    found_answer BOOLEAN DEFAULT 1,
    response_time_ms INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    top_k INTEGER,
    model_used TEXT
);
```

### Analytics Queries

#### Most Frequent Questions:
```sql
SELECT query, COUNT(*) as count 
FROM query_logs 
GROUP BY query 
ORDER BY count DESC 
LIMIT 10;
```

#### No Answer Rate:
```sql
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN found_answer = 0 THEN 1 ELSE 0 END) as no_answer_count
FROM query_logs;
```

#### Average Response Time:
```sql
SELECT AVG(response_time_ms) as avg_ms 
FROM query_logs;
```

---

## 🧪 Sample Test Queries

### Answerable Questions (from document):
- "What are the payment terms?"
- "How often do I have to pay service fees?"
- "What is the governing law?"
- "How can I terminate the agreement?"
- "What are the AWS security measures?"
- "What is AWS's liability limit?"
- "How are disputes resolved?"
- "What are the service levels?"

### Out-of-Scope Questions (hallucination test):
- "What is the price of EC2 instances?"
- "Who is the CEO of Amazon?"
- "What is AWS's market share?"
- "How do I deploy a Lambda function?"

---

## 🐛 Troubleshooting

### FastAPI won't start
**Error**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Make sure you're running from the project root directory.

### OpenAI API Key Not Found
**Error**: `openai.error.AuthenticationError`
**Solution**: Ensure your `.env` file exists with `OPENAI_API_KEY` set.

### Vector store not found
**Error**: `FileNotFoundError: Vector store not found`
**Solution**: Run `curl -X POST http://localhost:8000/ingest` first.

### Streamlit can't connect to backend
**Error**: `ConnectionError: Cannot connect to FastAPI backend`
**Solution**: Start FastAPI first, then Streamlit.

---

## 📝 Future Improvements

- [ ] Add support for multiple documents
- [ ] Implement document-level authentication
- [ ] Add caching layer for frequent queries
- [ ] Use PostgreSQL for production database
- [ ] Add Docker containerization
- [ ] Implement batch query processing
- [ ] Add model versioning and A/B testing
- [ ] Implement user session tracking
- [ ] Add PDF page preview for sources
- [ ] Integrate with LangSmith for monitoring

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the MIT LICENSE file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for the RAG framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Streamlit](https://streamlit.io/) for the dashboard
- [OpenAI](https://openai.com/) for embeddings and LLM
- [ChromaDB](https://www.trychroma.com/) for vector storage

---

---

## ⭐ Support

If you found this project helpful, please give it a ⭐ on GitHub!


---

**Built with ❤️ by Muskan Rastogi**
