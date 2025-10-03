"""
CrewAI Agents for YouTube Summarization with Multi-Provider Support
"""
from crewai import Agent
from langchain_ollama import ChatOllama
from src.config import Config
import os

# Set environment variables for litellm to properly handle Groq
os.environ["GROQ_API_KEY"] = Config.GROQ_API_KEY or ""

# Comprehensive telemetry and tracing disable
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = ""
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = ""
os.environ["OTEL_PYTHON_DISABLED_INSTRUMENTATIONS"] = "all"
os.environ["OTEL_TRACES_EXPORTER"] = "none"
os.environ["OTEL_METRICS_EXPORTER"] = "none"
os.environ["OTEL_LOGS_EXPORTER"] = "none"
os.environ["LITELLM_LOG"] = "ERROR"  # Reduce litellm logging

def create_llm(temperature: float = None):
    """Create the appropriate LLM instance based on configuration"""
    # Use local Ollama with codestral model
    temp = temperature or Config.MODEL_TEMPERATURE
    return create_ollama_llm(temp)

def create_groq_llm(temperature: float):
    """Create Groq LLM instance"""
    try:
        from langchain_groq import ChatGroq
        # Set the model with provider prefix for litellm compatibility
        llm = ChatGroq(
            groq_api_key=Config.GROQ_API_KEY,
            model=Config.GROQ_MODEL,
            temperature=temperature,
            max_tokens=Config.MAX_TOKENS
        )
        # Override the model attribute to include provider prefix
        llm.model = f"groq/{Config.GROQ_MODEL}"
        return llm
    except ImportError:
        print("⚠️ langchain-groq not installed. Install with: pip install langchain-groq")
        return create_ollama_llm(temperature)

def create_huggingface_llm(temperature: float):
    """Create HuggingFace LLM instance"""
    try:
        from langchain_community.llms import HuggingFaceHub
        return HuggingFaceHub(
            huggingfacehub_api_token=Config.HUGGINGFACE_API_KEY,
            repo_id="microsoft/DialoGPT-medium",
            model_kwargs={"temperature": temperature, "max_length": Config.MAX_TOKENS}
        )
    except ImportError:
        print("⚠️ langchain-community not installed. Falling back to Ollama")
        return create_ollama_llm(temperature)

def create_ollama_llm(temperature: float):
    """Create Ollama LLM instance"""
    print(f"🔧 Creating Ollama LLM with temperature: {temperature}")
    # Use ollama/ prefix as required by litellm/CrewAI
    model_name = f"ollama/{Config.OLLAMA_MODEL}"
    print(f"🤖 Using model: {model_name}")
    return ChatOllama(
        model=model_name,
        base_url=Config.OLLAMA_BASE_URL,
        temperature=temperature,
        max_retries=1,  # Allow 1 retry
        timeout=15,  # Keep short timeout for faster failure detection
        num_predict=100  # Keep short for speed
    )

def create_listener_agent():
    """Create the Listener Agent specialized in extracting key insights"""
    llm = create_llm(Config.LISTENER_TEMPERATURE)
    
    return Agent(
        role="Content Listener Specialist",
        goal="Extract and identify the most crucial insights, topics, and key points from video content with expert precision",
        backstory="""You are a Content Listener Specialist with exceptional ability to capture the essence of video content. 
        You have years of experience in content analysis across various domains including technology, business, education, 
        entertainment, and more. Your expertise lies in:
        
        - Identifying core themes and main topics
        - Extracting the most impactful quotes and statements  
        - Recognizing key arguments and supporting evidence
        - Understanding context and nuanced information
        - Distilling complex information into essential insights
        
        You focus on quality over quantity, ensuring only the most valuable and relevant content is captured.""",
        verbose=Config.CREW_VERBOSE,
        allow_delegation=False,
        llm=llm
    )

def create_content_writer_agent():
    """Create the Content Writer Agent specialized in crafting summaries"""
    llm = create_llm(Config.CONTENT_WRITER_TEMPERATURE)
    
    return Agent(
        role="Expert Content Writer",
        goal="Transform raw insights into compelling, well-structured, and highly valuable written summaries",
        backstory="""You are an Expert Content Writer with a proven track record of creating engaging, clear, 
        and actionable content. Your writing expertise spans multiple formats and audiences. You excel at:
        
        - Crafting compelling executive summaries that capture attention
        - Writing detailed, well-structured content that flows naturally
        - Creating actionable takeaways that provide real value
        - Adapting tone and style for different target audiences
        - Transforming complex information into accessible insights
        - Ensuring content is both informative and engaging
        
        Your summaries are known for their clarity, depth, and practical value.""",
        verbose=Config.CREW_VERBOSE,
        allow_delegation=False,
        llm=llm
    )

def create_critic_agent():
    """Create the Critic Agent specialized in quality validation"""
    llm = create_llm(Config.CRITIC_TEMPERATURE)
    
    return Agent(
        role="Quality Assurance Critic",
        goal="Rigorously evaluate content quality, accuracy, and relevance to ensure the highest standards",
        backstory="""You are a Quality Assurance Critic with an eagle eye for detail and a commitment to excellence. 
        Your role is crucial in maintaining the highest standards of content quality. Your expertise includes:
        
        - Evaluating content relevance and accuracy against source material
        - Assessing completeness and thoroughness of summaries
        - Identifying gaps, inconsistencies, or areas for improvement
        - Providing constructive feedback and specific recommendations
        - Ensuring content meets professional publication standards
        - Validating that summaries truly capture the essence of the original content
        
        You are known for your objectivity, thoroughness, and ability to provide actionable feedback.""",
        verbose=Config.CREW_VERBOSE,
        allow_delegation=False,
        llm=llm
    )
