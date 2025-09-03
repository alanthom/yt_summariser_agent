"""
Base agent class for all specialized agents
"""
from abc import ABC, abstractmethod
from typing import Any
from src.utils import openai_client
from src.config import Config

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, temperature: float = None):
        self.name = name
        self.temperature = temperature or Config.TEMPERATURE
        self.client = openai_client
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """Process input and return output"""
        pass
    
    def _make_request(self, user_message: str, response_format: str = None) -> str:
        """Make a request to OpenAI with system prompt"""
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": user_message}
        ]
        
        if response_format == "json":
            return self.client.structured_completion(messages, self.temperature)
        else:
            return self.client.chat_completion(messages, self.temperature)
    
    def __str__(self):
        return f"{self.name} Agent"
