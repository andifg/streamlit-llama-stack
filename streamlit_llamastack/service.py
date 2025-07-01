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
        Get list of available inference models from Llama Stack

        Returns:
            List of model names/identifiers
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

            logger.info(f"📊 Extracted models: {models}")
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

    def reset_session(self) -> None:
        """Reset the current session to start a fresh conversation"""
        logger.info("🔄 Resetting ReActAgent session")
        self._session_id = None
