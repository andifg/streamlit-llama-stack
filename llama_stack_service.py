"""
Llama Stack Service Module

This module handles all interactions with the Llama Stack server,
including model discovery, connection testing, and react agent chat.
"""

import logging
from typing import List, Optional
from llama_stack_client import LlamaStackClient

# Set up logging
logger = logging.getLogger(__name__)


class LlamaStackService:
    """Service class for interacting with Llama Stack server"""
    
    def __init__(self, base_url: str):
        """
        Initialize the Llama Stack service
        
        Args:
            base_url: The base URL of the Llama Stack server
        """
        self.base_url = base_url
        self._client = None
        self._agent_id = None
        self._session_id = None
    
    @property
    def client(self) -> LlamaStackClient:
        """Get or create the Llama Stack client"""
        if self._client is None:
            try:
                # Try minimal initialization first
                self._client = LlamaStackClient(base_url=self.base_url)
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
                        identifier = getattr(model, 'identifier', None)
                        if identifier:
                            models.append(str(identifier))
                            continue
                            
                        model_id = getattr(model, 'id', None)
                        if model_id:
                            models.append(str(model_id))
                            continue
                            
                        name = getattr(model, 'name', None)
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
                        logger.warning(f"⚠️ Error processing model {model}: {model_error}")
                        
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
            logger.info(f"🔍 Connection test successful, got response: {bool(models_response)}")
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
    
    def send_message(self, message: str, model_id: str, temperature: float = 0.7) -> Optional[str]:
        """
        Send a message using Llama Stack inference endpoint
        
        Args:
            message: The user message
            model_id: The model to use
            temperature: Sampling temperature
            
        Returns:
            Model response or None if error
        """
        try:
            logger.info(f"💬 Sending message to model {model_id}: {message[:50]}{'...' if len(message) > 50 else ''}")
            
            # Send message using the inference endpoint
            response = self.client.inference.chat_completion(
                model_id=model_id,
                messages=[{
                    "role": "user", 
                    "content": message
                }]
            )
            
            # Extract the response content
            if hasattr(response, 'completion_message') and hasattr(response.completion_message, 'content'):
                if isinstance(response.completion_message.content, str):
                    response_text = response.completion_message.content
                else:
                    response_text = str(response.completion_message.content)
            elif isinstance(response, dict):
                response_text = response.get('content', str(response))
            else:
                response_text = str(response)
            
            logger.info(f"✅ Model response received")
            return response_text
            
        except Exception as e:
            logger.error(f"❌ Error sending message to model: {e}")
            return f"❌ Error communicating with model: {str(e)}"
