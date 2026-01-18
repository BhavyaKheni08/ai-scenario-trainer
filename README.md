# 🎭 AI-Powered Roleplay Training Simulator

Transform passive PDF manuals into dynamic, high-pressure roleplay scenarios using Multi-Agent AI.

## 🚀 The Problem vs. The Solution

**The Old Way:** Companies hand new employees a 50-page PDF "policy manual" and hope they read it. Training is passive, boring, and untracked.

**The Solution:** This engine ingests that PDF and spawns an AI Actor that forces the user to apply the rules in a realistic chat simulation.

*   Is the user rude? The AI customer gets angrier.
*   Did the user break a rule? The AI Coach detects it instantly and grades them.

## ⚙️ How It Works (Agentic Architecture)

This project uses a **LangGraph Multi-Agent System** grounded in **RAG (Retrieval Augmented Generation)**.

1.  **The Architect:** Scans the uploaded manual, identifies "trap" clauses (e.g., "No ID, No Cash"), and designs a scenario to test them.
2.  **The Actor (Llama 3):** Plays the role of the difficult customer. It maintains a consistent persona and reacts dynamically to user sentiment.
3.  **The Coach:** Analyzes the chat logs post-simulation. It cites specific page numbers from the PDF where the user adhered to or violated policy.

## 🛠️ Tech Stack

*   **Orchestration:** LangGraph (Stateful Multi-Agent Workflows)
*   **LLM Engine:** Ollama (Running Llama 3 8B locally)
*   **Vector Database:** ChromaDB (For RAG/Knowledge retrieval)
*   **Backend:** FastAPI
*   **Frontend:** Streamlit
*   **Document Parsing:** PyPDF

## ⚡ Quick Start Guide

### Prerequisites
*   Python 3.10+
*   Ollama installed and running (`ollama run llama3`)

### 1. Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-scenario-trainer.git
cd ai-scenario-trainer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the System

You need two terminals open:

**Terminal 1: The Backend API**
```bash
uvicorn app.main:app --reload
```

**Terminal 2: The Frontend UI**
```bash
streamlit run ui/app.py
```

### 3. Usage

1.  Open http://localhost:8501.
2.  Upload a Training Manual PDF (e.g., Bank Policy Doc).
3.  Click "**Start New Simulation**".
4.  Chat with the AI "Customer" who will try to pressure you into breaking the rules.
5.  Click "**End & Grade**" to see if you passed.

## 📂 Project Structure

```bash
ai-scenario-trainer/
├── app/
│   ├── agents/          # LangGraph Nodes & State Logic
│   ├── api/             # FastAPI Endpoints
│   ├── services/        # RAG & Vector DB Logic
│   ├── schemas/         # Pydantic Models 
│   └── main.py          # App Entry Point
├── data/                # Local storage for ChromaDB & PDFs
├── ui/                  # Streamlit Interface
├── requirements.txt
└── README.md
```

## 📜 License

MIT License.
