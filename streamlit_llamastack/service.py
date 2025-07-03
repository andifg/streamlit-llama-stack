import os
import logging
from typing import List, Optional

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.react.agent import ReActAgent
from llama_stack_client.types.shared.user_message import UserMessage

# Set up logging
logger = logging.getLogger(__name__)


class LlamaStackService:
    """Service class for interacting with Llama Stack server using ReActAgent"""

    def __init__(self, base_url: str):
        """
        Initialize the Llama Stack service

        Args:
            base_url: The base URL of the Llama Stack server
        """
        self.base_url = base_url
        self._client: Optional[LlamaStackClient] = None
        self._agent: Optional[ReActAgent] = None
        self._session_id: Optional[str] = None

    @property
    def client(self) -> LlamaStackClient:
        """Get or create the Llama Stack client"""
        if self._client is None:
            try:
                # Try minimal initialization first
                self._client = LlamaStackClient(
                    base_url=self.base_url,
                    provider_data={
                        "tavily_search_api_key": os.getenv("TAVILY_SEARCH_API_KEY")
                    }
                )
            except Exception as e:
                logger.error(f"❌ Failed to create LlamaStackClient: {e}")
                raise
        return self._client

    def get_available_models(self) -> List[str]:
        """
        Get list of available LLM models from Llama Stack

        Returns:
            List of model names/identifiers (only LLM type models)
        """
        try:
            logger.info(f"🔗 Connecting to Llama Stack at: {self.base_url}")
            models_response = self.client.models.list()

            logger.info(f"🔍 Raw models response type: {type(models_response)}")
            logger.info(f"🔍 Raw models response: {models_response}")

            # Extract model names from the response - handle different formats
            models = []
            if models_response:
                for model in models_response:
                    try:
                        # Check if this is an LLM type model
                        logger.info(f"🔍 Model: {model}")
                        model_type = getattr(model, "model_type", None)
                        if model_type and str(model_type).lower() != "llm":
                            logger.info(f"🔍 Skipping non-LLM model: {model} (type: {model_type})")
                            continue

                        # Try different attribute names using getattr for safety
                        identifier = getattr(model, "identifier", None)
                        if identifier:
                            models.append(str(identifier))
                            continue

                        model_id = getattr(model, "id", None)
                        if model_id:
                            models.append(str(model_id))
                            continue

                        name = getattr(model, "name", None)
                        if name:
                            models.append(str(name))
                            continue

                        if isinstance(model, str):
                            models.append(model)
                            continue

                        # Fallback: convert to string and log
                        model_str = str(model)
                        models.append(model_str)
                        logger.info(f"🔍 Model fallback: {model_str}")

                    except Exception as model_error:
                        logger.warning(
                            f"⚠️ Error processing model {model}: {model_error}"
                        )

            logger.info(f"📊 Extracted LLM models: {models}")
            return models

        except Exception as e:
            logger.error(f"❌ Error fetching models from Llama Stack: {e}")
            return []

    def test_connection(self) -> bool:
        """
        Test if Llama Stack server is accessible

        Returns:
            True if connection successful, False otherwise
        """
        try:
            logger.info(f"🔍 Testing connection to Llama Stack at: {self.base_url}")
            models_response = self.client.models.list()
            logger.info(
                f"🔍 Connection test successful, got response: {bool(models_response)}"
            )
            return True
        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False

    def get_model_info(self, model_id: str) -> Optional[dict]:
        """
        Get detailed information about a specific model

        Args:
            model_id: The model identifier

        Returns:
            Model information dict or None if not found
        """
        try:
            # This would be implemented when we have the model details endpoint
            logger.info(f"🔍 Getting info for model: {model_id}")
            # Placeholder for future implementation
            return {"id": model_id, "status": "available"}
        except Exception as e:
            logger.error(f"❌ Error getting model info for {model_id}: {e}")
            return None

    def get_agent(self, model_id: str) -> ReActAgent:
        """
        Get or create a ReActAgent for the given model

        Args:
            model_id: The model to use for the agent

        Returns:
            ReActAgent instance
        """
        if self._agent is None:
            try:
                logger.info(f"🤖 Creating ReActAgent with model: {model_id}")

                # Create a ReActAgent with the specified model
                self._agent = ReActAgent(
                    client=self.client,
                    model=model_id,
                    tools=["builtin::websearch"],
                    instructions="You are a web search assistant. Always Use the provided brave_search tool to find the answer for the user prompt.",
                )
                logger.info("✅ ReActAgent created successfully")

            except Exception as e:
                logger.error(f"❌ Failed to create ReActAgent: {e}")
                raise

        return self._agent

    def get_session_id(self, model_id: str) -> str:
        """
        Get or create a session for the ReActAgent

        Args:
            model_id: The model to use

        Returns:
            Session ID
        """
        if self._session_id is None:
            try:
                agent = self.get_agent(model_id)
                session_name = f"streamlit_chat"
                session_id = agent.create_session(session_name=session_name)
                self._session_id = str(session_id)  # Ensure it's a string
                logger.info(f"📝 Created new session: {self._session_id}")
            except Exception as e:
                logger.error(f"❌ Failed to create session: {e}")
                raise

        # At this point _session_id should never be None due to the above logic
        assert self._session_id is not None
        return self._session_id

    def send_message(
        self, message: str, model_id: str, temperature: float = 0.7
    ) -> Optional[str]:
        """
        Send a message using ReActAgent

        Args:
            message: The user message
            model_id: The model to use
            temperature: Sampling temperature (note: may not be used by ReActAgent)

        Returns:
            ReActAgent response or None if error
        """
        try:
            logger.info(
                f"💬 Sending message to ReActAgent with {model_id}: {message[:50]}{'...' if len(message) > 50 else ''}"
            )

            # Get agent and session
            agent = self.get_agent(model_id)
            session_id = self.get_session_id(model_id)

            # Create a turn with the agent (non-streaming)
            user_message = UserMessage(content=message, role="user")
            response = agent.create_turn(
                messages=[user_message], session_id=session_id, stream=False
            )

            # Extract the response content from Turn object
            response_text = "Sorry, I couldn't process your request properly."

            try:
                # When stream=False, response should be a Turn object with output_message
                # Use getattr to safely access attributes for type checking
                logger.info(f"RESPONSE: {response}")
                output_message = getattr(response, "output_message", None)
                if output_message:
                    content = getattr(output_message, "content", None)
                    if isinstance(content, str):
                        response_text = content
                    else:
                        response_text = (
                            str(content) if content else "No content in response"
                        )
                else:
                    response_text = f"No output message in response: {str(response)}"

            except Exception as extract_error:
                logger.warning(f"⚠️ Error extracting response content: {extract_error}")
                response_text = "Sorry, I encountered an error processing the response."

            logger.info(f"✅ ReActAgent response received")
            return response_text

        except Exception as e:
            logger.error(f"❌ Error communicating with ReActAgent: {e}")
            return f"❌ Error communicating with ReActAgent: {str(e)}"

    def send_message_with_turn_details(
        self, message: str, model_id: str, temperature: float = 0.7
    ) -> dict:
        """
        Send a message using ReActAgent and return detailed turn information

        Args:
            message: The user message
            model_id: The model to use
            temperature: Sampling temperature (note: may not be used by ReActAgent)

        Returns:
            Dictionary containing turn details including reasoning steps and tool usage
        """
        try:
            logger.info(
                f"💬 Sending message to ReActAgent with {model_id}: {message[:50]}{'...' if len(message) > 50 else ''}"
            )

            # Get agent and session
            agent = self.get_agent(model_id)
            session_id = self.get_session_id(model_id)

            # Create a turn with the agent (non-streaming)
            user_message = UserMessage(content=message, role="user")
            turn = agent.create_turn(
                messages=[user_message], session_id=session_id, stream=False
            )

            # Extract detailed turn information
            turn_details = {
                "success": True,
                "final_response": "Sorry, I couldn't process your request properly.",
                "reasoning_steps": [],
                "tool_usage": [],
                "turn_id": "unknown",  # Will be updated below
                "status": getattr(turn, "status", "unknown"),
                "raw_turn": str(turn)
            }

            # Debug: Log all available attributes of the turn object
            logger.info(f"🔍 Turn object type: {type(turn)}")
            logger.info(f"🔍 Turn object dir: {dir(turn)}")
            logger.info(f"🔍 Turn object attributes: {[attr for attr in dir(turn) if not attr.startswith('_')]}")
            
            # Try different possible attribute names for turn ID
            possible_id_attrs = ['id', 'turn_id', 'identifier', 'uuid', 'turn_uuid']
            for attr in possible_id_attrs:
                value = getattr(turn, attr, None)
                if value:
                    logger.info(f"🔍 Found turn ID in attribute '{attr}': {value}")
                    turn_details["turn_id"] = str(value)
                    break
            else:
                logger.warning(f"⚠️ No turn ID found in any of the expected attributes: {possible_id_attrs}")
                # Try to extract from string representation
                turn_str = str(turn)
                if "id=" in turn_str:
                    import re
                    match = re.search(r'id=([^,\s]+)', turn_str)
                    if match:
                        turn_details["turn_id"] = match.group(1)
                        logger.info(f"🔍 Extracted turn ID from string: {turn_details['turn_id']}")

            try:
                logger.info(f"🔍 Analyzing turn structure: {turn}")
                
                # Extract steps from the turn
                steps = getattr(turn, "steps", [])
                if steps:
                    logger.info(f"🔍 Found {len(steps)} steps in turn")
                    
                    for i, step in enumerate(steps):
                        step_type = getattr(step, "step_type", "unknown")
                        step_id = getattr(step, "step_id", f"step_{i}")
                        
                        logger.info(f"🔍 Processing step {i+1}: {step_type} (ID: {step_id})")
                        
                        if step_type == "inference":
                            # Handle inference step
                            api_model_response = getattr(step, "api_model_response", None)
                            if api_model_response:
                                content = getattr(api_model_response, "content", "")
                                role = getattr(api_model_response, "role", "assistant")
                                stop_reason = getattr(api_model_response, "stop_reason", "")
                                
                                # Check if this step has tool calls
                                tool_calls = getattr(api_model_response, "tool_calls", [])
                                if tool_calls:
                                    # This is a reasoning step that decided to use tools
                                    reasoning_content = f"Assistant decided to use tools. Stop reason: {stop_reason}"
                                    turn_details["reasoning_steps"].append({
                                        "type": "inference",
                                        "content": reasoning_content,
                                        "step_id": step_id,
                                        "tool_calls": len(tool_calls)
                                    })
                                    
                                    # Extract tool call details
                                    for tool_call in tool_calls:
                                        tool_name = getattr(tool_call, "tool_name", "unknown_tool")
                                        arguments = getattr(tool_call, "arguments", {})
                                        call_id = getattr(tool_call, "call_id", "")
                                        
                                        turn_details["tool_usage"].append({
                                            "tool_name": tool_name,
                                            "arguments": arguments,
                                            "call_id": call_id,
                                            "step_id": step_id,
                                            "status": "requested"
                                        })
                                else:
                                    # This is a final response step
                                    if content:
                                        turn_details["final_response"] = content
                                        turn_details["reasoning_steps"].append({
                                            "type": "final_response",
                                            "content": f"Final response generated. Stop reason: {stop_reason}",
                                            "step_id": step_id
                                        })
                        
                        elif step_type == "tool_execution":
                            # Handle tool execution step
                            tool_calls = getattr(step, "tool_calls", [])
                            tool_responses = getattr(step, "tool_responses", [])
                            
                            logger.info(f"🔍 Tool execution step: {len(tool_calls)} calls, {len(tool_responses)} responses")
                            
                            # Match tool responses to tool calls
                            for tool_response in tool_responses:
                                call_id = getattr(tool_response, "call_id", "")
                                content = getattr(tool_response, "content", "")
                                tool_name = getattr(tool_response, "tool_name", "unknown_tool")
                                
                                # Find matching tool call
                                for tool_usage in turn_details["tool_usage"]:
                                    if tool_usage.get("call_id") == call_id:
                                        tool_usage["output"] = content
                                        tool_usage["status"] = "completed"
                                        tool_usage["step_id"] = step_id
                                        break
                                
                                # If no matching tool call found, add as new entry
                                else:
                                    turn_details["tool_usage"].append({
                                        "tool_name": tool_name,
                                        "call_id": call_id,
                                        "output": content,
                                        "step_id": step_id,
                                        "status": "completed"
                                    })

                # Extract turn metadata
                turn_details["created_at"] = getattr(turn, "created_at", None)
                turn_details["completed_at"] = getattr(turn, "completed_at", None)

            except Exception as extract_error:
                logger.warning(f"⚠️ Error extracting turn details: {extract_error}")
                turn_details["success"] = False
                turn_details["error"] = str(extract_error)

            logger.info(f"✅ ReActAgent turn details extracted")
            return turn_details

        except Exception as e:
            logger.error(f"❌ Error communicating with ReActAgent: {e}")
            return {
                "success": False,
                "error": f"Error communicating with ReActAgent: {str(e)}",
                "final_response": f"❌ Error communicating with ReActAgent: {str(e)}",
                "reasoning_steps": [],
                "tool_usage": [],
                "turn_id": "error",
                "status": "error"
            }

    def reset_session(self) -> None:
        """Reset the current session to start a fresh conversation"""
        logger.info("🔄 Resetting ReActAgent session")
        self._session_id = None
