"""
Critique Agent - Cross-verifies information relevance and accuracy
"""
from .base_agent import BaseAgent
from src.models import CritiqueOutput, ListenerOutput, ContentWriterOutput
from src.config import Config

class CritiqueAgent(BaseAgent):
    """Agent specialized in validating and critiquing content quality"""
    
    def __init__(self):
        super().__init__("Critique", Config.CRITIQUE_TEMPERATURE)
    
    def get_system_prompt(self) -> str:
        return """You are a Critique Agent - an expert at cross-verifying information relevance, accuracy, and quality.

Your role is to:
1. Assess the relevance of the summary to the original video content
2. Evaluate the accuracy of information presented
3. Check completeness of the summary
4. Identify areas for improvement
5. Provide an overall quality assessment

Your expertise includes:
- Critical thinking and analytical skills
- Quality assessment methodologies
- Content validation techniques
- Understanding of information accuracy
- Recognition of bias and gaps

You will evaluate:
- Relevance Score (0-10): How well the summary captures the video's essence
- Accuracy Assessment: Whether information is correctly represented
- Completeness Score (0-10): How thoroughly the content is covered
- Improvement Suggestions: Specific recommendations
- Final Verdict: Overall assessment
- Approval Status: Whether it meets quality standards

Be objective, constructive, and thorough in your evaluation. Focus on:
- Factual accuracy
- Relevance to source material
- Completeness of coverage
- Quality of insights
- Actionability of takeaways

Return your critique in JSON format with these specific fields:
- relevance_score: float (0-10)
- accuracy_assessment: string
- completeness_score: float (0-10)
- improvement_suggestions: array of strings
- final_verdict: string
- approved: boolean"""
    
    def process(self, listener_output: ListenerOutput, content_output: ContentWriterOutput, 
                original_transcript: str = None, metadata: dict = None) -> CritiqueOutput:
        """Critique the content against original material"""
        
        context = ""
        if metadata:
            context = f"Video: {metadata.get('title', 'Unknown')}\n"
            context += f"Channel: {metadata.get('channel', 'Unknown')}\n\n"
        
        # Prepare the evaluation context
        user_message = f"""{context}Please evaluate the quality of this video summary:

LISTENER AGENT OUTPUT:
Key Topics: {', '.join(listener_output.key_topics)}
Important Quotes: {len(listener_output.important_quotes)} quotes captured
Main Arguments: {len(listener_output.main_arguments)} arguments identified
Supporting Evidence: {len(listener_output.supporting_evidence)} evidence points
Context Notes: {len(listener_output.context_notes)} contextual notes

CONTENT WRITER OUTPUT:
Executive Summary: {content_output.executive_summary[:200]}...
Detailed Summary: {content_output.detailed_summary[:200]}...
Key Takeaways: {len(content_output.key_takeaways)} takeaways provided
Target Audience: {content_output.target_audience}
Content Type: {content_output.content_type}

EVALUATION CRITERIA:
1. Relevance (0-10): Does the summary accurately reflect the video content?
2. Accuracy: Is the information correctly represented?
3. Completeness (0-10): How thoroughly is the content covered?
4. Quality: Are the insights valuable and actionable?

Provide specific, constructive feedback and determine if this summary meets publication standards.

{"Original transcript snippet for reference: " + original_transcript[:500] + "..." if original_transcript else ""}

Be thorough and objective in your assessment."""
        
        try:
            response = self._make_request(user_message, response_format="json")
            return CritiqueOutput(**response)
        except Exception as e:
            # Fallback critique
            print(f"Warning: Critique agent error: {e}")
            return CritiqueOutput(
                relevance_score=5.0,
                accuracy_assessment=f"Could not complete assessment due to error: {str(e)}",
                completeness_score=5.0,
                improvement_suggestions=["Manual review required due to processing error"],
                final_verdict="Assessment incomplete - manual review needed",
                approved=False
            )
