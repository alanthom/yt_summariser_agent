"""
Data models for the YouTube Summarizer with CrewAI
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class VideoMetadata(BaseModel):
    """Metadata for a YouTube video"""
    title: str
    video_id: str
    url: str
    duration: Optional[str] = None
    channel: Optional[str] = None

class CrewOutput(BaseModel):
    """Output from CrewAI execution"""
    raw_output: str = Field(description="Raw text output from the crew")
    token_usage: Optional[Dict[str, Any]] = Field(default=None, description="Token usage information")
    timestamp: datetime = Field(default_factory=datetime.now)

class ProcessedSummary(BaseModel):
    """Processed and structured summary from CrewAI output"""
    executive_summary: str = Field(description="High-level overview of the content")
    detailed_summary: str = Field(description="Comprehensive analysis of the video")
    key_takeaways: List[str] = Field(description="Actionable insights")
    key_topics: List[str] = Field(description="Main topics discussed")
    important_quotes: List[str] = Field(description="Notable quotes")
    target_audience: str = Field(description="Intended audience")
    content_category: str = Field(description="Type of content")
    
    # Quality metrics
    relevance_score: Optional[float] = Field(default=None, description="Relevance score from critic")
    completeness_score: Optional[float] = Field(default=None, description="Completeness score from critic")
    quality_approved: Optional[bool] = Field(default=None, description="Whether approved by critic")
    improvement_suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")
    
    timestamp: datetime = Field(default_factory=datetime.now)

class FinalSummary(BaseModel):
    """Final aggregated summary with all outputs"""
    video_metadata: VideoMetadata
    crew_output: CrewOutput
    processed_summary: ProcessedSummary
    processing_timestamp: datetime = Field(default_factory=datetime.now)
    
    def to_markdown(self) -> str:
        """Convert to markdown format for easy reading"""
        md = f"""# YouTube Video Summary

## Video Information
- **Title**: {self.video_metadata.title}
- **URL**: {self.video_metadata.url}
- **Channel**: {self.video_metadata.channel or 'Unknown'}
- **Duration**: {self.video_metadata.duration or 'Unknown'}
- **Content Category**: {self.processed_summary.content_category}

## Executive Summary
{self.processed_summary.executive_summary}

## Detailed Summary
{self.processed_summary.detailed_summary}

## Key Takeaways
"""
        for i, takeaway in enumerate(self.processed_summary.key_takeaways, 1):
            md += f"{i}. {takeaway}\n"
        
        md += f"""
## Main Topics Discussed
"""
        for topic in self.processed_summary.key_topics:
            md += f"- {topic}\n"
            
        if self.processed_summary.important_quotes:
            md += f"""
## Notable Quotes
"""
            for quote in self.processed_summary.important_quotes:
                md += f"> {quote}\n\n"
        
        # Quality assessment section
        if self.processed_summary.relevance_score is not None:
            md += f"""
## Quality Assessment
- **Relevance Score**: {self.processed_summary.relevance_score}/10
"""
        if self.processed_summary.completeness_score is not None:
            md += f"- **Completeness Score**: {self.processed_summary.completeness_score}/10\n"
        
        if self.processed_summary.quality_approved is not None:
            status = '✅ Approved' if self.processed_summary.quality_approved else '❌ Needs Improvement'
            md += f"- **Status**: {status}\n"
        
        if self.processed_summary.improvement_suggestions:
            md += f"""
## Improvement Suggestions
"""
            for suggestion in self.processed_summary.improvement_suggestions:
                md += f"- {suggestion}\n"

        md += f"""
## Target Audience
{self.processed_summary.target_audience}

---
*Summary generated using CrewAI and {self.video_metadata.video_id} on {self.processing_timestamp.strftime('%Y-%m-%d %H:%M:%S')}*

## Raw CrewAI Output
<details>
<summary>Click to expand raw output</summary>

```
{self.crew_output.raw_output}
```
</details>
"""
        return md
