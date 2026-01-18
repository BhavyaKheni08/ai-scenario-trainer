# 🎭 AI-Powered Roleplay Training Simulator

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-FF6F00?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit)

> **An interactive training platform that transforms static PDF manuals into dynamic, high-pressure roleplay scenarios. Uses Local LLMs (Llama 3) to simulate difficult customers and automated grading agents to score employee performance.**

---

## 🏗️ Architecture

This system uses a **Stateful Multi-Agent** workflow orchestrated by **LangGraph**. The workflow transitions between specific "modes" (Setup, Simulation, Evaluation) to create a complete training loop.

```mermaid
graph TD
    User("👤 Trainee") --> UI["Streamlit Dashboard"]
    UI --> API("FastAPI Endpoint")
    
    API --> Architect["🏗️ Architect Agent"]
    Architect -->|Generates Scenario| Actor["🎭 Actor Agent"]
    
    Actor <-->|Roleplay Loop| User
    
    User -->|End Session| Coach{"👮 Coach Agent"}
    Coach -->|Retrieves Policy| DB("🔍 Vector Store (RAG)")
    
    Coach -->|Pass/Fail Logic| Report("📊 Final Scorecard")
    Report --> UI
✨ Features
🧠 Behavioral Simulation: The Actor Agent adopts a specific persona (e.g., "Angry VIP", "Confused Senior") to test user soft skills dynamically.

📚 RAG-Based Compliance: Retrieves specific policy clauses from your uploaded PDF (via ChromaDB) to ensure the AI "Coach" grades based on your actual rules.

⚖️ Automated Grading: The Coach Agent reviews the chat logs after the session, citing specific page numbers where the user passed or failed protocols.

🔒 Privacy First: Designed to run entirely with Local LLMs (Ollama) — sensitive training data never leaves your infrastructure.

⚡ Real-Time Feedback: Instant feedback loops compared to traditional passive reading or manual peer review.

🚀 Quick Start
Prerequisites
Python 3.10+ installed.

Ollama running locally with llama3 pulled.

1. Clone & Configure
Bash
git clone [https://github.com/BhavyaKheni08/ai-scenario-trainer.git](https://github.com/BhavyaKheni08/ai-scenario-trainer.git)
cd ai-scenario-trainer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
2. Run the System
You need to run the Backend and Frontend in separate terminals.

Terminal 1: Start Backend API

Bash
uvicorn app.main:app --reload
Terminal 2: Start Frontend Dashboard

Bash
streamlit run ui/app.py
3. Access the System
Mission Control Dashboard: http://localhost:8501

API Documentation: http://localhost:8000/docs

🛠️ Usage Workflow
Upload Policy: Go to the sidebar and upload a PDF (e.g., Bank_Teller_Manual.pdf).

Initialize: Click "Start Simulation". The Architect Agent will read the PDF and generate a "Trap Scenario" (e.g., a customer demanding a cash withdrawal without ID).

Roleplay: Chat with the AI. Try to de-escalate the situation without breaking the rules defined in the PDF.

Evaluation: Click "End & Grade". The Coach Agent will analyze your transcript and give you a score (0-10) with specific feedback.

🧪 Testing
We include a health check endpoint to verify that your Local LLM (Ollama) and Vector Database are connected:

Bash
curl http://localhost:8000/health
📜 License
Distributed under the MIT License. See LICENSE for more information.
