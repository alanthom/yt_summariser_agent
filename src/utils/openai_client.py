"""
OpenAI integration utilities
"""
import openai
from typing import Dict, Any, Optional
import json
from src.config import Config

class OpenAIClient:
    """Wrapper for OpenAI API interactions"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def chat_completion(self, messages: list, temperature: float = None, max_tokens: int = None, response_format: str = None) -> str:
        """Make a chat completion request"""
        try:
            kwargs = {
                "model": Config.OPENAI_MODEL,
                "messages": messages,
                "temperature": temperature or Config.TEMPERATURE,
                "max_tokens": max_tokens or Config.MAX_TOKENS
            }
            
            if response_format == "json":
                kwargs["response_format"] = {"type": "json_object"}
            
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def structured_completion(self, messages: list, temperature: float = None) -> Dict[Any, Any]:
        """Make a completion request expecting JSON response"""
        try:
            response_text = self.chat_completion(
                messages=messages,
                temperature=temperature,
                response_format="json"
            )
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {str(e)}")
        except Exception as e:
            raise Exception(f"Structured completion error: {str(e)}")

# Global instance
openai_client = OpenAIClient()
