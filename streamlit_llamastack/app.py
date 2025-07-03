import logging
from typing import List, Optional

import streamlit as st

from streamlit_llamastack.service import LlamaStackService

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger.info("🚀 Streamlit Ollama Chat starting...")

# Configure the page
st.set_page_config(
    page_title="Llama Stack Chat",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

# Llama Stack configuration
llama_stack_url = st.sidebar.text_input(
    "Llama Stack URL",
    value="http://localhost:8321",
    help="URL of your Llama Stack server (handles both model discovery and chat)",
)


# Create Llama Stack service instance
@st.cache_resource
def get_llama_stack_service(base_url: str) -> LlamaStackService:
    """Get cached Llama Stack service instance"""
    return LlamaStackService(base_url)


# Get available models from Llama Stack
@st.cache_data(ttl=30)  # Cache for 30 seconds to avoid repeated API calls
def get_llama_stack_models(base_url: str) -> List[str]:
    """Get list of available LLM models from Llama Stack with caching"""
    service = get_llama_stack_service(base_url)
    return service.get_available_models()


# Load available models
available_models = get_llama_stack_models(llama_stack_url)

model_name: Optional[str] = None
if available_models:
    logger.info(f"📊 Found {len(available_models)} LLM models: {available_models}")
    st.sidebar.success(f"✅ Found {len(available_models)} LLM model(s)")
    model_name = st.sidebar.selectbox(
        "LLM Model", options=available_models, index=0, help="Select the LLM model to use"
    )
else:
    logger.warning("⚠️ No LLM models found in Llama Stack!")
    st.sidebar.error("❌ No LLM models found in Llama Stack")
    st.sidebar.markdown("**Please:**")
    st.sidebar.markdown("1. Ensure Llama Stack is running: `INFERENCE_MODEL=llama3.2:3b uv run --with llama-stack llama stack build --template ollama --image-type venv --run`")
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
    help="Controls randomness in the response",
)



# Display options
show_turn_details = st.sidebar.checkbox(
    "Show Turn Details by Default",
    value=False,
    help="Automatically expand reasoning steps and tool usage sections"
)

# Main app
st.title("🦙 Llama Stack Chat")
st.caption("AI-powered chat interface using Llama Stack")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
logger.info(f"📝 Displaying {len(st.session_state.messages)} messages from history")
for i, message in enumerate(st.session_state.messages):
    logger.info(f"📝 Message {i+1}: role={message['role']}, has_turn_details={'turn_details' in message}")
    with st.chat_message(message["role"]):
        # For assistant messages with turn details, show the final response prominently
        if message["role"] == "assistant" and "turn_details" in message:
            turn_details = message["turn_details"]
            # Use final_response from turn_details if available, otherwise use message content
            final_response = turn_details.get("final_response", message["content"])
            
            # Show final response with nice formatting
            st.markdown("### 🤖 Final Response")
            st.markdown(final_response)
            
            # Display turn details for assistant messages if available
            # Show turn metadata
            with st.expander("📊 Turn Details", expanded=show_turn_details):
                st.markdown("#### 📈 Turn Information")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Turn ID:** {turn_details.get('turn_id', 'N/A')}")
                    if turn_details.get('created_at'):
                        st.markdown(f"**Started:** {turn_details['created_at']}")
                with col2:
                    st.markdown(f"**Status:** {turn_details.get('status', 'N/A')}")
                    if turn_details.get('completed_at'):
                        st.markdown(f"**Completed:** {turn_details['completed_at']}")
            
            # Show reasoning steps if any
            if turn_details.get("reasoning_steps"):
                with st.expander("🧠 Reasoning Steps", expanded=show_turn_details):
                    st.markdown("#### 🔍 Internal Reasoning Process")
                    for i, step in enumerate(turn_details["reasoning_steps"], 1):
                        step_type = step.get('type', 'unknown')
                        step_id = step.get('step_id', 'N/A')
                        content = step.get('content', 'No content')
                        
                        st.markdown(f"**Step {i} ({step_type}):** {content}")
                        st.markdown(f"*Step ID: {step_id}*")
                        
                        if step.get('tool_calls'):
                            st.markdown(f"*Tool calls in this step: {step['tool_calls']}*")
            
            # Show tool usage if any
            if turn_details.get("tool_usage"):
                with st.expander("🔧 Tool Usage", expanded=show_turn_details):
                    st.markdown("#### 🛠️ External Tool Execution")
                    for i, tool in enumerate(turn_details["tool_usage"], 1):
                        tool_name = tool.get('tool_name', 'Unknown Tool')
                        status = tool.get('status', 'unknown')
                        step_id = tool.get('step_id', 'N/A')
                        call_id = tool.get('call_id', 'N/A')
                        
                        st.markdown(f"**Tool {i}:** {tool_name} ({status})")
                        st.markdown(f"*Step ID: {step_id} | Call ID: {call_id}*")
                        
                        if tool.get('arguments'):
                            st.markdown("**Arguments:**")
                            st.json(tool['arguments'])
                        
                        if tool.get('output'):
                            st.markdown("**Output:**")
                            # Try to parse JSON output for better display
                            try:
                                import json
                                output_data = json.loads(tool['output'])
                                st.json(output_data)
                            except:
                                st.text(tool['output'])
        else:
            # For user messages or simple assistant messages, show content normally
            st.markdown(message["content"])

# Function to call Llama Stack with turn details
def call_llama_stack_with_details(prompt: str, model: str, temperature: float) -> dict:
    """Call the Llama Stack API with the given prompt and return turn details"""
    try:
        service = get_llama_stack_service(llama_stack_url)
        return service.send_message_with_turn_details(prompt, model, temperature)

    except Exception as e:
        logger.error(f"❌ Error calling Llama Stack: {e}")
        return {
            "success": False,
            "error": f"❌ Unexpected error: {str(e)}",
            "final_response": f"❌ Unexpected error: {str(e)}",
            "reasoning_steps": [],
            "tool_usage": [],
            "turn_id": "error",
            "status": "error"
        }


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
                st.cache_data.clear()
                st.cache_resource.clear()
                st.rerun()  # Refresh the page to reload models

# Chat input
if model_name:  # Only show chat input if a model is available
    if prompt := st.chat_input("What would you like to ask?"):
        logger.info(
            f"💬 User message: {prompt[:50]}{'...' if len(prompt) > 50 else ''}"
        )

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                logger.info(
                    f"🤖 Generating response with {model_name} (temp: {temperature})"
                )
                turn_details = call_llama_stack_with_details(prompt, model_name, temperature)
                
                if turn_details["success"]:
                    logger.info(f"✅ Response generated with turn ID: {turn_details['turn_id']}")
                    
                    # Display reasoning steps if any
                    if turn_details["reasoning_steps"]:
                        with st.expander("🧠 Reasoning Steps", expanded=show_turn_details):
                            st.markdown("#### 🔍 Internal Reasoning Process")
                            for i, step in enumerate(turn_details["reasoning_steps"], 1):
                                step_type = step.get('type', 'unknown')
                                step_id = step.get('step_id', 'N/A')
                                content = step.get('content', 'No content')
                                
                                st.markdown(f"**Step {i} ({step_type}):** {content}")
                                st.markdown(f"*Step ID: {step_id}*")
                                
                                if step.get('tool_calls'):
                                    st.markdown(f"*Tool calls in this step: {step['tool_calls']}*")
                    
                    # Display tool usage if any
                    if turn_details["tool_usage"]:
                        with st.expander("🔧 Tool Usage", expanded=show_turn_details):
                            st.markdown("#### 🛠️ External Tool Execution")
                            for i, tool in enumerate(turn_details["tool_usage"], 1):
                                tool_name = tool.get('tool_name', 'Unknown Tool')
                                status = tool.get('status', 'unknown')
                                step_id = tool.get('step_id', 'N/A')
                                call_id = tool.get('call_id', 'N/A')
                                
                                st.markdown(f"**Tool {i}:** {tool_name} ({status})")
                                st.markdown(f"*Step ID: {step_id} | Call ID: {call_id}*")
                                
                                if tool.get('arguments'):
                                    st.markdown("**Arguments:**")
                                    st.json(tool['arguments'])
                                
                                if tool.get('output'):
                                    st.markdown("**Output:**")
                                    # Try to parse JSON output for better display
                                    try:
                                        import json
                                        output_data = json.loads(tool['output'])
                                        st.json(output_data)
                                    except:
                                        st.text(tool['output'])
                    
                    # Display final response with nice formatting
                    final_response = turn_details["final_response"]
                    st.markdown("---")
                    st.markdown("### 🤖 Final Response")
                    st.markdown(final_response)
                    
                    # Store turn details in session state for later reference
                    turn_info = {
                        "turn_id": turn_details["turn_id"],
                        "status": turn_details["status"],
                        "reasoning_steps": turn_details["reasoning_steps"],
                        "tool_usage": turn_details["tool_usage"],
                        "final_response": final_response,
                        "created_at": turn_details.get("created_at"),
                        "completed_at": turn_details.get("completed_at")
                    }
                    
                    # Add assistant response to chat history with turn details
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": final_response,
                        "turn_details": turn_info
                    })
                else:
                    error_msg = turn_details.get("error", "Unknown error occurred")
                    logger.error(f"❌ Error: {error_msg}")
                    st.error(f"❌ Error: {error_msg}")
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"❌ Error: {error_msg}"
                    })
                
                # Rerun to display the complete updated chat history
                st.rerun()
else:
    st.info(
        "🔄 Please ensure Llama Stack is running and models are available to start chatting."
    )

# Clear chat history and reset session
with st.sidebar:
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Chat"):
            logger.info(
                f"🗑️ Clearing chat history ({len(st.session_state.messages)} messages)"
            )
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Agent"):
            logger.info("🔄 Resetting ReActAgent session")
            service = get_llama_stack_service(llama_stack_url)
            service.reset_session()
            st.session_state.messages = []
            st.success("ReActAgent session reset!")
            st.rerun()

# Info section
with st.sidebar:
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.markdown(
        """
    This app uses Llama Stack **ReActAgent** for AI-powered conversations with advanced step-by-step reasoning capabilities.
    
    **Features:**
    - 🧠 **ReActAgent** with sophisticated reasoning patterns
    - 🔧 LLM model discovery and selection (LLM type only)
    - ⚙️ Temperature control for response creativity
    - 🔄 Session management for conversation context
    - 📊 **Turn Details** - View reasoning steps and tool usage
    
    **Default port:**
    - Llama Stack: 8321
    
    **Getting started:**
    1. Run `ollama serve` (backend for Llama Stack)
    2. Pull models: `ollama pull llama3.2:3b`  
    3. Run `INFERENCE_MODEL=llama3.2:3b uv run --with llama-stack llama stack build --template ollama --image-type venv --run`
    4. Start chatting with the ReActAgent!
    
    **ReActAgent Features:**
    - **ReAct (Reasoning + Acting)** pattern for problem solving
    - Step-by-step reasoning with thought processes
    - Maintains conversation context within sessions
    - Can be extended with tools and capabilities
    - **Turn Details**: View internal reasoning steps and tool usage
    """
    )
