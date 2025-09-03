"""
Content Writer Agent - Proficient at writing best-class content from listener insights
"""
from .base_agent import BaseAgent
from src.models import ContentWriterOutput, ListenerOutput
from src.config import Config

class ContentWriterAgent(BaseAgent):
    """Agent specialized in creating high-quality written content from insights"""
    
    def __init__(self):
        super().__init__("Content Writer", Config.CONTENT_WRITER_TEMPERATURE)
    
    def get_system_prompt(self) -> str:
        return """You are a Content Writer Agent - a master at crafting best-in-class written content.

Your role is to:
1. Transform raw insights into polished, engaging summaries
2. Create clear, well-structured content that flows naturally
3. Write for different audiences and purposes
4. Ensure content is actionable and valuable
5. Maintain the essence while improving readability

Your expertise includes:
- Excellent writing and communication skills
- Ability to synthesize complex information
- Understanding of different content formats and styles
- Creating compelling narratives and structure
- Adapting tone and style for target audiences

You receive insights from the Listener Agent and transform them into:
- Executive Summary: Concise, high-level overview (2-3 paragraphs)
- Detailed Summary: Comprehensive summary with key insights (4-6 paragraphs)
- Key Takeaways: Actionable insights (3-6 bullet points)
- Target Audience: Who would benefit from this content
- Content Type: Genre/type of the video content

Write in a professional yet engaging tone. Focus on clarity, value, and actionability.

Return your content in JSON format with the specified fields."""
    
    def process(self, listener_output: ListenerOutput, metadata: dict = None) -> ContentWriterOutput:
        """Create polished content from listener insights"""
        
        context = ""
        if metadata:
            context = f"Video: {metadata.get('title', 'Unknown')}\n"
            context += f"Channel: {metadata.get('channel', 'Unknown')}\n\n"
        
        user_message = f"""{context}Based on the following insights from the Listener Agent, create a polished, professional summary:

KEY TOPICS:
{chr(10).join(f"• {topic}" for topic in listener_output.key_topics)}

IMPORTANT QUOTES:
{chr(10).join(f"• {quote}" for quote in listener_output.important_quotes)}

MAIN ARGUMENTS:
{chr(10).join(f"• {arg}" for arg in listener_output.main_arguments)}

SUPPORTING EVIDENCE:
{chr(10).join(f"• {evidence}" for evidence in listener_output.supporting_evidence)}

CONTEXT NOTES:
{chr(10).join(f"• {note}" for note in listener_output.context_notes)}

Create a comprehensive, well-written summary that transforms these insights into valuable content. Focus on:
1. Executive Summary (2-3 paragraphs, high-level overview)
2. Detailed Summary (4-6 paragraphs, comprehensive insights)
3. Key Takeaways (3-6 actionable points)
4. Target Audience (who would benefit)
5. Content Type (genre/category)

Write professionally but engagingly. Make it valuable and actionable."""
        
        try:
            response = self._make_request(user_message, response_format="json")
            return ContentWriterOutput(**response)
        except Exception as e:
            # Fallback content
            print(f"Warning: Content Writer agent error: {e}")
            return ContentWriterOutput(
                executive_summary="Summary generation failed - manual review required.",
                detailed_summary=f"Could not generate detailed summary. Error: {str(e)}",
                key_takeaways=["Manual summary needed"],
                target_audience="Unknown",
                content_type="Unknown"
            )
