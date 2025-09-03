"""
Listener Agent - Expert at capturing the crux and key pointers from content
"""
from .base_agent import BaseAgent
from src.models import ListenerOutput
from src.config import Config
import json

class ListenerAgent(BaseAgent):
    """Agent specialized in listening and extracting key insights from video content"""
    
    def __init__(self):
        super().__init__("Listener", Config.LISTENER_TEMPERATURE)
    
    def get_system_prompt(self) -> str:
        return """You are a Listener Agent - an expert at capturing the crux and key pointers from video content.

Your role is to:
1. Identify the main topics and themes discussed
2. Extract the most important quotes and statements
3. Capture the core arguments and points being made
4. Note supporting evidence and examples
5. Provide essential contextual information

You have domain expertise across various fields and excel at:
- Distilling complex information into key insights
- Identifying the most impactful statements and ideas
- Understanding context and nuance
- Recognizing patterns and connections
- Extracting actionable information

Focus on quality over quantity. Capture only the most essential and impactful elements.

Return your analysis in JSON format with these fields:
- key_topics: Main topics discussed (max 8 items)
- important_quotes: Notable quotes or statements (max 6 items)
- main_arguments: Core arguments or points made (max 6 items)
- supporting_evidence: Evidence or examples provided (max 6 items)
- context_notes: Important contextual information (max 5 items)

Be precise, insightful, and focus on the most valuable content."""
    
    def process(self, transcript: str, metadata: dict = None) -> ListenerOutput:
        """Process video transcript and extract key insights"""
        
        context = f"Video Title: {metadata.get('title', 'Unknown')}\n" if metadata else ""
        context += f"Channel: {metadata.get('channel', 'Unknown')}\n" if metadata and metadata.get('channel') else ""
        
        user_message = f"""{context}
Please analyze the following video transcript and extract the key insights:

TRANSCRIPT:
{transcript}

Extract the most important elements following your role as a Listener Agent."""
        
        try:
            response = self._make_request(user_message, response_format="json")
            return ListenerOutput(**response)
        except Exception as e:
            # Fallback with basic extraction
            print(f"Warning: Listener agent error: {e}")
            return ListenerOutput(
                key_topics=["Analysis failed - manual review needed"],
                important_quotes=[],
                main_arguments=["Could not extract arguments"],
                supporting_evidence=[],
                context_notes=[f"Error during processing: {str(e)}"]
            )
