import streamlit as st
import requests
import json
import sys
import os
from typing import Optional

# Configure the page
st.set_page_config(
    page_title="Ollama Chat",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

# Ollama configuration
ollama_url = st.sidebar.text_input(
    "Ollama URL",
    value="http://localhost:11434",
    help="URL of your Ollama server"
)

model_name = st.sidebar.selectbox(
    "Model",
    options=["llama3.2:3b", "llama3.1:8b", "codellama:7b", "mistral:7b", "llama2:7b"],
    index=0,
    help="Select the model to use"
)

# Chat parameters
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Controls randomness in the response"
)

# Main app
st.title("🦙 Ollama Chat")
st.markdown("Chat with your local Ollama models")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to call Ollama API
def call_ollama(prompt: str, model: str, temperature: float) -> Optional[str]:
    """Call the Ollama API with the given prompt"""
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        response = requests.post(
            f"{ollama_url}/api/generate",
            json=payload,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        return result.get("response", "No response received from the model.")
        
    except requests.exceptions.ConnectionError:
        return "❌ Connection error: Could not connect to Ollama. Please check if Ollama is running."
    except requests.exceptions.Timeout:
        return "❌ Timeout error: The request took too long. Please try again."
    except requests.exceptions.HTTPError as e:
        return f"❌ HTTP error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# Function to get available models
def get_available_models() -> list:
    """Get list of available models from Ollama"""
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        response.raise_for_status()
        data = response.json()
        return [model["name"] for model in data.get("models", [])]
    except:
        return []

# Function to test connection
def test_connection() -> bool:
    """Test if Ollama is accessible"""
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

# Connection status and model refresh
with st.sidebar:
    st.markdown("---")
    st.subheader("🔌 Connection Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Test Connection"):
            with st.spinner("Testing..."):
                if test_connection():
                    st.success("✅ Connected!")
                else:
                    st.error("❌ No connection")
    
    with col2:
        if st.button("Refresh Models"):
            with st.spinner("Loading models..."):
                models = get_available_models()
                if models:
                    st.success(f"Found {len(models)} models")
                    st.write("Available models:")
                    for model in models:
                        st.write(f"• {model}")
                else:
                    st.warning("No models found")

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_ollama(prompt, model_name, temperature)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat history
with st.sidebar:
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Info section
with st.sidebar:
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.markdown("""
    This app connects directly to Ollama running locally.
    
    **Default Ollama port:** 11434
    
    **Getting started:**
    1. Install Ollama
    2. Run `ollama serve`
    3. Pull a model: `ollama pull llama3.2:3b`
    4. Start chatting!
    """)

# Programmatic startup - allows running with 'python3 app.py'
if __name__ == "__main__":
    import subprocess
    import sys
    
    # Get the current file path
    current_file = os.path.abspath(__file__)
    
    # Run streamlit with the current file
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", current_file,
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]) 