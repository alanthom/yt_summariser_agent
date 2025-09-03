"""
Custom LLM wrapper for CrewAI to avoid litellm provider issues
"""
from langchain.llms.base import LLM
from langchain_ollama import ChatOllama
from typing import Optional, List, Any
import requests
import json

class OllamaLLMWrapper(LLM):
    """Custom Ollama LLM wrapper for CrewAI"""
    
    model: str
    base_url: str
    temperature: float
    
    def __init__(self, model: str, base_url: str, temperature: float = 0.7):
        super().__init__()
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
    
    @property
    def _llm_type(self) -> str:
        return "ollama"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
    ) -> str:
        """Call the Ollama API directly"""
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature
                }
            }
            
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return "Error: Unable to generate response"
    
    @property
    def _identifying_params(self) -> dict:
        """Get the identifying parameters"""
        return {
            "model": self.model,
            "base_url": self.base_url,
            "temperature": self.temperature
        }
