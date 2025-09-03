"""
Configuration settings for the YouTube Summarizer using CrewAI and Ollama
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Ollama Settings (Free Open Source)
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")  # Use faster llama3.2 model
    
    # Model Settings
    MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))
    
    # Agent-specific temperatures
    LISTENER_TEMPERATURE = 0.3  # More focused for extraction
    CONTENT_WRITER_TEMPERATURE = 0.7  # More creative for writing
    CRITIC_TEMPERATURE = 0.2  # Very focused for validation
    
    # Output Settings
    OUTPUT_DIR = "outputs"
    SAVE_INTERMEDIATE_OUTPUTS = True
    
    # CrewAI Settings
    CREW_VERBOSE = True
    CREW_MEMORY = False  # Set to True if you want agents to remember across runs
    
    # Alternative Models (if you have API keys)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Free tier available
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Free tier available
    
    # Auto-detection settings
    USE_GROQ_IF_AVAILABLE = True  # Automatically use Groq if API key is present
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")  # Use valid Groq model
    
    @classmethod
    def get_preferred_llm_provider(cls):
        """Determine which LLM provider to use based on availability"""
        if cls.USE_GROQ_IF_AVAILABLE and cls.GROQ_API_KEY:
            return "groq"
        elif cls.HUGGINGFACE_API_KEY:
            return "huggingface"
        else:
            return "ollama"
    
    @classmethod
    def validate(cls):
        """Validate configuration based on preferred provider"""
        provider = cls.get_preferred_llm_provider()
        
        if provider == "groq":
            if not cls.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is required but not found in environment")
            # Groq doesn't need local validation - API key is validated on first request
            return True
            
        elif provider == "huggingface":
            if not cls.HUGGINGFACE_API_KEY:
                raise ValueError("HUGGINGFACE_API_KEY is required but not found in environment")
            return True
            
        else:  # Ollama validation
            try:
                import requests
                response = requests.get(f"{cls.OLLAMA_BASE_URL}/api/tags", timeout=5)
                if response.status_code != 200:
                    raise ValueError(f"Cannot connect to Ollama at {cls.OLLAMA_BASE_URL}")
                
                # Check if the specified model exists
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                if cls.OLLAMA_MODEL not in model_names:
                    available = ", ".join(model_names) if model_names else "No models found"
                    raise ValueError(
                        f"Model '{cls.OLLAMA_MODEL}' not found in Ollama.\n"
                        f"Available models: {available}\n"
                        f"Install the model with: ollama pull {cls.OLLAMA_MODEL}"
                    )
                
                return True
            except requests.exceptions.RequestException:
                raise ValueError(
                    f"Cannot connect to Ollama at {cls.OLLAMA_BASE_URL}\n"
                    "Please ensure Ollama is running. Start it with: ollama serve"
                )
            except Exception as e:
                raise ValueError(f"Configuration validation failed: {str(e)}")
    
    @classmethod
    def get_available_models(cls):
        """Get list of available Ollama models"""
        try:
            import requests
            response = requests.get(f"{cls.OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except:
            return []
