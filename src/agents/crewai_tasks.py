"""
CrewAI Tasks for YouTube Summarization
"""
from crewai import Task

def create_listener_task(transcript: str, metadata: dict):
    """Create task for the Listener Agent"""
    context = f"Video Title: {metadata.get('title', 'Unknown')}\n"
    context += f"Channel: {metadata.get('channel', 'Unknown')}\n" if metadata.get('channel') else ""
    
    return Task(
        description=f"""Analyze this video content and extract comprehensive insights with expert precision:

{context}

TRANSCRIPT:
{transcript}

Your analysis should include:

1. EXECUTIVE SUMMARY OVERVIEW (2-3 sentences):
   - Provide a high-level summary of what this video is about
   - Capture the main purpose and core message

2. DETAILED KEY INSIGHTS BREAKDOWN:
   - Identify 4-6 core themes and main topics discussed
   - Extract the most impactful quotes and statements
   - Recognize key arguments and supporting evidence
   - Note any important data, statistics, or examples

3. IMPORTANT QUOTES AND EVIDENCE:
   - Select 3-5 most significant quotes from the content
   - Include any compelling data points or statistics mentioned
   - Highlight unique insights or perspectives shared

4. CONTEXT AND BACKGROUND INFORMATION:
   - Identify the target audience and purpose
   - Note the style and format of the content
   - Understand any industry context or background needed

Focus on quality over quantity. Extract only the most valuable and relevant insights that truly capture the essence of this content.""",
        expected_output="""A comprehensive analysis containing:
- Executive Summary Overview: 2-3 sentence high-level summary
- Detailed Key Insights: 4-6 core themes with supporting details
- Important Quotes: 3-5 most significant quotes from the content
- Evidence and Data: Key statistics, examples, or data points
- Context and Background: Target audience, purpose, and relevant context

Format as clear, organized sections with bullet points.""",
        output_file="outputs/listener_analysis.md",
        agent=None  # Will be assigned when creating the crew
    )

def create_content_writer_task():
    """Create task for the Content Writer Agent"""
    return Task(
        description="""Transform the insights from the Listener Agent into a polished, professional summary.

Using the extracted insights (key topics, quotes, arguments, evidence, and context), create:

1. EXECUTIVE SUMMARY (2-3 paragraphs): A compelling high-level overview that captures the essence
2. DETAILED SUMMARY (4-6 paragraphs): Comprehensive summary with key insights and learnings
3. KEY TAKEAWAYS (4-6 items): Actionable insights that viewers can apply
4. TARGET AUDIENCE: Identify who would benefit most from this content
5. CONTENT CATEGORY: Classify the type/genre of content

Write in a professional yet engaging tone. Ensure the content flows naturally and provides real value.
Make it clear, actionable, and compelling for readers.""",
        expected_output="""A well-structured summary containing:
- Executive Summary: 2-3 paragraph high-level overview
- Detailed Summary: 4-6 paragraph comprehensive analysis
- Key Takeaways: 4-6 actionable bullet points
- Target Audience: Clear description of intended audience
- Content Category: Classification of content type

All content should be polished, engaging, and professional.""",
        output_file="outputs/content_summary.md",
        agent=None  # Will be assigned when creating the crew
    )

def create_critic_task():
    """Create task for the Critic Agent"""
    return Task(
        description="""Evaluate the content summary created by the Content Writer against the original insights and provide quality assessment.

Review the summary for:

1. RELEVANCE (Score 0-10): How well does the summary capture the original video's essence?
2. ACCURACY: Is the information correctly represented and faithful to the source?
3. COMPLETENESS (Score 0-10): How thoroughly does the summary cover the important content?
4. QUALITY: Are the insights valuable, actionable, and well-presented?
5. IMPROVEMENT AREAS: What specific enhancements could be made?

Provide constructive feedback and determine if the summary meets publication standards.
Be objective, thorough, and specific in your assessment.""",
        expected_output="""A comprehensive quality assessment including:
- Relevance Score: 0-10 rating with justification
- Accuracy Assessment: Evaluation of information correctness
- Completeness Score: 0-10 rating with explanation
- Quality Review: Assessment of value and presentation
- Improvement Suggestions: 3-5 specific recommendations
- Final Verdict: Overall assessment and approval status
- Approved: Yes/No decision on publication readiness

Provide specific, actionable feedback for any areas needing improvement.""",
        output_file="outputs/quality_assessment.md",
        agent=None  # Will be assigned when creating the crew
    )
