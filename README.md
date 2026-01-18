🎭 AI-Powered Roleplay Training Simulator
An interactive training platform that transforms static PDF manuals into dynamic, high-pressure roleplay scenarios. Uses Local LLMs (Llama 3) to simulate difficult customers and automated grading agents to score employee performance.

🏗️ Architecture
This system uses a Stateful Multi-Agent workflow orchestrated by LangGraph. The workflow transitions between specific "modes" (Setup, Simulation, Evaluation) to create a complete training loop.

Code snippet
graph TD
    Upload("📄 PDF Manual Upload") --> DB("🔍 Vector Store (ChromaDB)")
    Start("🚀 Start Simulation") --> Architect["🏗️ Architect Agent"]
    DB --> Architect
    Architect --> Actor["🎭 Actor Agent (The 'Customer')"]
    
    Actor <-->|Chat Loop| User("👤 Trainee")
    
    User -->|End Session| Coach{"👮 Coach Agent"}
    DB --> Coach
    Coach -->|Grading Logic| Report("📊 Final Scorecard")
    
    subgraph "Frontend Interface"
    User --> UI["Streamlit Dashboard"]
    Report --> UI
    end
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
git clone https://github.com/BhavyaKheni08/ai-scenario-trainer.git
cd ai-scenario-trainer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
2. Start the Backend (API)
The FastAPI server handles the LangGraph workflow and State management.

Bash
uvicorn app.main:app --reload
API will be available at http://localhost:8000/docs

3. Start the Frontend (UI)
Launch the interactive training dashboard in a new terminal.

Bash
streamlit run ui/app.py
Access the dashboard at http://localhost:8501

🛠️ Usage Guide
Upload Policy: Go to the sidebar and upload a PDF (e.g., Bank_Teller_Manual.pdf).

Initialize: Click "Start Simulation". The Architect Agent will read the PDF and generate a "Trap Scenario" (e.g., a customer demanding a cash withdrawal without ID).

Roleplay: Chat with the AI. Try to de-escalate the situation without breaking the rules defined in the PDF.

Evaluation: Click "End & Grade". The Coach Agent will analyze your transcript and give you a score (0-10) with specific feedback.

🧪 Project Structure
Bash
ai-scenario-trainer/
├── app/
│   ├── agents/          # LangGraph Nodes (Architect, Actor, Coach)
│   ├── api/             # FastAPI Routes
│   ├── services/        # RAG & PDF Ingestion Logic
│   └── main.py          # Application Entry Point
├── data/                # Vector Store persistence
├── ui/                  # Streamlit Interface code
└── requirements.txt     # Python Dependencies
📜 License
Distributed under the MIT License. See LICENSE for more information.
