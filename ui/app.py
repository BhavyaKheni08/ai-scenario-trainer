import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_URL = "http://localhost:8000/api/v1"

def init_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "simulation_active" not in st.session_state:
        st.session_state.simulation_active = False

def main():
    st.set_page_config(
        page_title="AI Scenario Trainer",
        page_icon="🤖",
        layout="wide"
    )
    
    init_session()

    st.title("🤖 AI-Powered Roleplay Trainer")
    st.markdown("---")
    
    # --- Sidebar: Configuration & Controls ---
    with st.sidebar:
        st.header("Configuration")
        
        # 1. File Uploader
        uploaded_file = st.file_uploader("Upload Training Manual (PDF)", type=["pdf"])
        if uploaded_file is not None:
            if st.button("Upload & Ingest"):
                files = {"file": uploaded_file}
                try:
                    with st.spinner("Ingesting manual..."):
                        response = requests.post(f"{API_URL}/upload-manual", files=files)
                        if response.status_code == 200:
                            data = response.json()
                            st.success(f"Success! {data.get('chunks_created')} chunks created.")
                        else:
                            st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
        
        st.divider()
        
        # 2. Start Simulation
        if st.button("Start New Simulation", type="primary"):
            try:
                with st.spinner("Architecting Scenario..."):
                    payload = {"session_id": st.session_state.session_id}
                    response = requests.post(f"{API_URL}/simulation/start", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.messages = [] # Clear history
                        
                        # Add initial AI message
                        ai_msg = data.get("message")
                        if ai_msg:
                            st.session_state.messages.append({"role": "assistant", "content": ai_msg})
                        
                        st.session_state.simulation_active = True
                        st.rerun()
                    else:
                        st.error(f"Failed to start: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

        st.divider()
        
        # 3. Grading
        if st.session_state.simulation_active:
            if st.button("End & Grade Simulation"):
                try:
                    with st.spinner("Analyzing performance..."):
                        payload = {"session_id": st.session_state.session_id}
                        response = requests.post(f"{API_URL}/simulation/grade", json=payload)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.balloons()
                            st.metric(label="Final Score", value=f"{data.get('score')}/10")
                            st.info(f"Feedback: {data.get('feedback')}")
                            st.session_state.simulation_active = False # Disable chat
                        else:
                            st.error(f"Grading failed: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

    # --- Main Chat Interface ---
    if not st.session_state.messages and not st.session_state.simulation_active:
        st.info("👈 Upload a manual and click 'Start New Simulation' to begin.")
    else:
        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat Input
        if st.session_state.simulation_active:
            if prompt := st.chat_input("Type your response..."):
                # 1. Add User Message
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # 2. Get AI Response
                try:
                    payload = {
                        "session_id": st.session_state.session_id,
                        "message": prompt
                    }
                    
                    with st.spinner("Thinking..."):
                        response = requests.post(f"{API_URL}/simulation/chat", json=payload)
                        
                        if response.status_code == 200:
                            data = response.json()
                            ai_msg = data.get("message")
                            
                            st.session_state.messages.append({"role": "assistant", "content": ai_msg})
                            with st.chat_message("assistant"):
                                st.markdown(ai_msg)
                        else:
                            st.error(f"Error: {response.text}")
                except Exception as e:
                     st.error(f"Connection Error: {e}")

if __name__ == "__main__":
    main()
