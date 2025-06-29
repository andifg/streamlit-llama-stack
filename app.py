import streamlit as st
import logging
from typing import Optional
from llama_stack_service import LlamaStackService

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("🚀 Streamlit Ollama Chat starting...")

# Configure the page
st.set_page_config(
    page_title="Llama Stack Chat",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

# Llama Stack configuration
llama_stack_url = st.sidebar.text_input(
    "Llama Stack URL",
    value="http://localhost:8321",
    help="URL of your Llama Stack server (handles both model discovery and chat)"
)

# Create Llama Stack service instance
@st.cache_resource
def get_llama_stack_service(base_url: str) -> LlamaStackService:
    """Get cached Llama Stack service instance"""
    return LlamaStackService(base_url)

# Get available models from Llama Stack
@st.cache_data(ttl=30)  # Cache for 30 seconds to avoid repeated API calls
def get_llama_stack_models(base_url: str):
    """Get list of available inference models from Llama Stack with caching"""
    service = get_llama_stack_service(base_url)
    return service.get_available_models()

# Load available models
available_models = get_llama_stack_models(llama_stack_url)

if available_models:
    logger.info(f"📊 Found {len(available_models)} models: {available_models}")
    st.sidebar.success(f"✅ Found {len(available_models)} model(s)")
    model_name = st.sidebar.selectbox(
        "Model",
        options=available_models,
        index=0,
        help="Select the model to use"
    )
else:
    logger.warning("⚠️ No models found in Llama Stack!")
    st.sidebar.error("❌ No models found in Llama Stack")
    st.sidebar.markdown("**Please:**")
    st.sidebar.markdown("1. Ensure Llama Stack is running: `llama stack run`")
    st.sidebar.markdown("2. Ensure Ollama is running with models")
    st.sidebar.markdown("3. Click 'Refresh Models' below")
    model_name = None

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
st.title("🦙 Llama Stack Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to call Llama Stack
def call_llama_stack(prompt: str, model: str, temperature: float) -> Optional[str]:
    """Call the Llama Stack API with the given prompt"""
    try:
        service = get_llama_stack_service(llama_stack_url)
        return service.send_message(prompt, model, temperature)
        
    except Exception as e:
        logger.error(f"❌ Error calling Llama Stack: {e}")
        return f"❌ Unexpected error: {str(e)}"

# This function is now replaced by the cached get_ollama_models() function above

# Function to test connection
def test_connection() -> bool:
    """Test if Llama Stack is accessible"""
    service = get_llama_stack_service(llama_stack_url)
    return service.test_connection()

# Connection status and model refresh
with st.sidebar:
    st.markdown("---")
    st.subheader("🔌 Connection Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Test Connection"):
            logger.info("🔍 Testing connection to Llama Stack...")
            with st.spinner("Testing..."):
                if test_connection():
                    logger.info("✅ Connection successful!")
                    st.success("✅ Connected!")
                else:
                    logger.error("❌ Connection failed!")
                    st.error("❌ No connection")
    
    with col2:
        if st.button("Refresh Models"):
            with st.spinner("Loading models..."):
                # Clear the cache to force reload
                get_llama_stack_models.clear()
                get_llama_stack_service.clear()
                st.rerun()  # Refresh the page to reload models

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if model_name:  # Only show chat input if a model is available
    if prompt := st.chat_input("What would you like to ask?"):
        logger.info(f"💬 User message: {prompt[:50]}{'...' if len(prompt) > 50 else ''}")
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                logger.info(f"🤖 Generating response with {model_name} (temp: {temperature})")
                response = call_llama_stack(prompt, model_name, temperature)
                if response:
                    logger.info(f"✅ Response generated ({len(response)} chars)")
                else:
                    logger.error("❌ No response received")
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("🔄 Please ensure Llama Stack is running and models are available to start chatting.")

# Clear chat history
with st.sidebar:
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        logger.info(f"🗑️ Clearing chat history ({len(st.session_state.messages)} messages)")
        st.session_state.messages = []
        st.rerun()

# Info section
with st.sidebar:
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.markdown("""
    This app uses Llama Stack for both model discovery and chat generation.
    
    **Default port:**
    - Llama Stack: 8321
    
    **Getting started:**
    1. Run `ollama serve` (backend for Llama Stack)
    2. Pull models: `ollama pull llama3.2:3b`  
    3. Run `llama stack run --port 8321`
    4. Start chatting!
    """)

 