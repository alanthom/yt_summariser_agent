"""
File I/O utilities
"""
import os
import json
from datetime import datetime
from typing import Any
from src.config import Config
from src.models import FinalSummary

class FileManager:
    """Handles file operations for the summarizer"""
    
    @staticmethod
    def ensure_output_dir():
        """Ensure output directory exists"""
        if not os.path.exists(Config.OUTPUT_DIR):
            os.makedirs(Config.OUTPUT_DIR)
    
    @staticmethod
    def save_json(data: Any, filename: str) -> str:
        """Save data as JSON file"""
        FileManager.ensure_output_dir()
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        
        # Convert Pydantic models to dict if necessary
        if hasattr(data, 'dict'):
            data = data.dict()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        return filepath
    
    @staticmethod
    def save_markdown(content: str, filename: str) -> str:
        """Save content as markdown file"""
        FileManager.ensure_output_dir()
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    @staticmethod
    def save_summary(summary: FinalSummary) -> tuple:
        """Save complete summary in multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_id = summary.video_metadata.video_id
        
        # Generate filenames
        json_filename = f"summary_{video_id}_{timestamp}.json"
        md_filename = f"summary_{video_id}_{timestamp}.md"
        
        # Save files
        json_path = FileManager.save_json(summary, json_filename)
        md_path = FileManager.save_markdown(summary.to_markdown(), md_filename)
        
        return json_path, md_path
    
    @staticmethod
    def save_intermediate(data: Any, stage: str, video_id: str) -> str:
        """Save intermediate processing data"""
        if not Config.SAVE_INTERMEDIATE_OUTPUTS:
            return ""
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{stage}_{video_id}_{timestamp}.json"
        return FileManager.save_json(data, filename)
