"""
Simplified CrewAI Tasks for YouTube Summarization - Testing Mode
"""
from crewai import Task

def create_listener_task(transcript: str, metadata: dict):
    """Create minimal task for the Listener Agent"""
    return Task(
        description=f"""Analyze: {metadata.get('title', 'Video')}

Transcript: {transcript[:100]}...

Write one sentence about the main topic.""",
        expected_output="One sentence about the main topic",
        output_file="outputs/listener_analysis.md"
    )

def create_content_writer_task():
    """Create minimal task for the Content Writer Agent"""
    return Task(
        description="""Write one sentence summary.""",
        expected_output="One sentence summary",
        output_file="outputs/content_summary.md"
    )

def create_critic_task():
    """Create minimal task for the Critic Agent"""
    return Task(
        description="""Say "Good summary" or "Needs improvement".""",
        expected_output="Good summary or Needs improvement",
        output_file="outputs/critic_review.md"
    )
