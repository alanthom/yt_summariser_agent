"""
CrewAI Tasks for YouTube Summarization
"""
from crewai import Task

def create_listener_task(transcript: str, metadata: dict):
    """Create task for the Listener Agent"""
    context = f"Video: {metadata.get('title', 'Unknown')}\n"
    context += f"Channel: {metadata.get('channel', 'Unknown')}\n" if metadata.get('channel') else ""
    
    return Task(
        description=f"""Analyze this video and extract key insights:

{context}

TRANSCRIPT:
{transcript}

Extract:
1. SUMMARY (2-3 sentences): Main topic and purpose
2. KEY THEMES (3-4 items): Core topics discussed  
3. IMPORTANT QUOTES (2-3 items): Most significant statements
4. AUDIENCE: Who this content is for

Keep it concise and focused.""",
        expected_output="""Analysis with:
- Summary: 2-3 sentences
- Key Themes: 3-4 bullet points
- Important Quotes: 2-3 significant quotes
- Target Audience: Brief description

Format as organized sections.""",
        output_file="outputs/listener_analysis.md",
        agent=None  # Will be assigned when creating the crew
    )

def create_content_writer_task():
    """Create task for the Content Writer Agent"""
    return Task(
        description="""Transform the listener's insights into a polished summary.

Create:
1. EXECUTIVE SUMMARY (2 paragraphs): High-level overview
2. DETAILED SUMMARY (3 paragraphs): Key insights and findings  
3. KEY TAKEAWAYS (3-4 items): Actionable insights
4. CONTENT TYPE: Brief classification

Write clearly and professionally.""",
        expected_output="""Well-structured summary with:
- Executive Summary: 2 paragraphs
- Detailed Summary: 3 paragraphs  
- Key Takeaways: 3-4 bullet points
- Content Type: Brief classification

Professional tone, clear structure.""",
        output_file="outputs/content_summary.md",
        agent=None  # Will be assigned when creating the crew
    )

def create_critic_task():
    """Create task for the Critic Agent"""
    return Task(
        description="""Review the content summary for quality.

Evaluate:
1. RELEVANCE (Score 1-10): How well does it capture the video?
2. ACCURACY: Is information correctly represented?
3. COMPLETENESS (Score 1-10): Coverage of important content  
4. IMPROVEMENTS: 2-3 specific suggestions

Be objective and constructive.""",
        expected_output="""Quality assessment with:
- Relevance Score: 1-10 with brief reason
- Accuracy Assessment: Brief evaluation
- Completeness Score: 1-10 with brief reason  
- Improvement Suggestions: 2-3 specific points
- Final Verdict: Approved/Needs Review

Concise, actionable feedback.""",
        output_file="outputs/quality_assessment.md",
        agent=None  # Will be assigned when creating the crew
    )
