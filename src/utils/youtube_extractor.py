"""
YouTube transcript extraction utilities
"""
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
from typing import Optional, Tuple
import requests
from bs4 import BeautifulSoup

class YouTubeExtractor:
    """Handles YouTube video transcript and metadata extraction"""
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def get_video_metadata(video_id: str) -> dict:
        """Get video metadata from YouTube"""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            response = requests.get(url, timeout=10)  # Add timeout for network requests
            response.raise_for_status()  # Raise HTTPError for bad responses
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('meta', property='og:title')
            title = title_tag['content'] if title_tag else f"Video {video_id}"
            
            # Extract channel name
            channel_tag = soup.find('meta', property='og:video:tag')
            channel = channel_tag.get('content') if channel_tag else "Unknown Channel"
            
            return {
                'title': title,
                'channel': channel,
                'video_id': video_id,
                'url': url
            }
        except requests.exceptions.RequestException as e:
            print(f"Network error while fetching metadata for video ID {video_id}: {e}")
            return {
                'title': f"Video {video_id}",
                'channel': "Unknown Channel",
                'video_id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }
        except Exception as e:
            print(f"Unexpected error while fetching metadata for video ID {video_id}: {e}")
            return {
                'title': f"Video {video_id}",
                'channel': "Unknown Channel",
                'video_id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }
    
    @staticmethod
    def get_transcript(video_id: str, languages: list = ['en', 'en-US']) -> Optional[str]:
        """Get transcript for a YouTube video"""
        try:
            # Create API instance and get transcript
            api = YouTubeTranscriptApi()
            transcript_obj = api.fetch(video_id, languages=languages)
            
            # Extract the transcript data from snippets
            transcript_data = transcript_obj.snippets
            
            # Format transcript as plain text
            formatter = TextFormatter()
            transcript = formatter.format_transcript(transcript_data)
            
            return transcript
            
        except Exception as e:
            print(f"Error getting transcript for video ID {video_id}: {e}")
            try:
                # Try to get any available transcript
                api = YouTubeTranscriptApi()
                transcript_list = api.list(video_id)
                
                # Find an English transcript
                for transcript in transcript_list:
                    if transcript.language_code in ['en', 'en-US', 'en-GB']:
                        transcript_obj = transcript.fetch()
                        formatter = TextFormatter()
                        transcript_text = formatter.format_transcript(transcript_obj.snippets)
                        return transcript_text
                
                # If no English transcript, try the first available
                if transcript_list:
                    transcript_obj = transcript_list[0].fetch()
                    formatter = TextFormatter()
                    transcript_text = formatter.format_transcript(transcript_obj.snippets)
                    return transcript_text
                
            except Exception as e2:
                print(f"Error getting any transcript for video ID {video_id}: {e2}")
                
            # Return a sample transcript for testing when real transcript is not available
            return """[DEMO MODE - Transcript not available]
                
This is a sample transcript for testing the YouTube summarizer system. 
In a real scenario, this would contain the actual spoken content from the video.

Key topics that would typically be covered:
- Main subject matter of the video
- Important points and insights shared
- Key quotes or statements
- Supporting evidence or examples
- Conclusions and takeaways

This demo content allows you to test the AI agents and see how they would process 
and summarize actual video content when transcripts are available."""
    
    @classmethod
    def process_youtube_url(cls, url: str) -> Tuple[Optional[dict], Optional[str]]:
        """Process YouTube URL and return metadata and transcript"""
        video_id = cls.extract_video_id(url)
        if not video_id:
            return None, None
            
        metadata = cls.get_video_metadata(video_id)
        transcript = cls.get_transcript(video_id)
        
        return metadata, transcript
