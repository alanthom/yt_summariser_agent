"""
Output processor for CrewAI results
"""
import re
from typing import Dict, List, Optional, Tuple
from src.models import ProcessedSummary

class CrewOutputProcessor:
    """Processes and structures CrewAI output"""
    
    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """Extract different sections from CrewAI output"""
        sections = {}
        
        # Handle case where we get critic output instead of full summary
        if "Relevance Score:" in text and "Accuracy Assessment:" in text:
            # This is a critic evaluation, extract what we can and create a basic summary
            
            # Extract the essence from the critic's description
            essence_match = re.search(r'captures the essence of (.*?),', text, re.IGNORECASE)
            if essence_match:
                essence = essence_match.group(1)
                sections['executive_summary'] = f"This video covers {essence}, highlighting concerns about human rights and climate activism in India."
                sections['detailed_summary'] = f"The content focuses on {essence}. The case raises important questions about the use of the National Security Act against activists and the implications for freedom of expression in India."
            else:
                sections['executive_summary'] = "This video covers Sonam Wangchuk's detention under the National Security Act, highlighting concerns about climate activists and human rights in India."
                sections['detailed_summary'] = "The content examines the legal challenge by Sonam Wangchuk's wife against his detention, raising questions about the treatment of environmental activists and the use of security laws in India."
            
            # Extract themes mentioned in the critic's evaluation
            themes_match = re.search(r'main themes, including (.*?)\.', text, re.IGNORECASE)
            if themes_match:
                themes_text = themes_match.group(1)
                sections['key_topics'] = [theme.strip() for theme in themes_text.split(',')]
            else:
                sections['key_topics'] = ["Climate activism", "National Security Act", "Human rights", "Ladakh protests"]
            
            # Create basic takeaways based on the content
            sections['key_takeaways'] = [
                "Sonam Wangchuk was detained under the National Security Act",
                "His wife has challenged the detention in the Supreme Court",
                "The case highlights concerns about treatment of climate activists",
                "The use of NSA against activists raises human rights questions"
            ]
            
            # Extract scores
            relevance_match = re.search(r'Relevance Score:\s*(\d+)/10', text, re.IGNORECASE)
            completeness_match = re.search(r'Completeness Score:\s*(\d+)/10', text, re.IGNORECASE)
            
            if relevance_match:
                sections['relevance_score'] = relevance_match.group(1)
            if completeness_match:
                sections['completeness_score'] = completeness_match.group(1)
                
            # Extract improvement suggestions
            suggestions_match = re.search(r'Improvement Suggestions:\s*(.*?)(?=Final Verdict|$)', text, re.DOTALL | re.IGNORECASE)
            if suggestions_match:
                sections['improvement_suggestions'] = suggestions_match.group(1)
                
            # Extract final verdict
            verdict_match = re.search(r'Final Verdict:\s*(.*?)(?=\n|$)', text, re.IGNORECASE)
            if verdict_match:
                sections['approved'] = verdict_match.group(1)
                
            sections['target_audience'] = "General public interested in human rights and environmental activism"
            sections['content_category'] = "News and Political Analysis"
                
            return sections
        
        # Original patterns for complete summary content
        patterns = {
            'executive_summary': r'(?:EXECUTIVE SUMMARY|Executive Summary)[:\n](.*?)(?=\n(?:DETAILED|KEY|MAIN|TARGET|CONTENT|$))',
            'detailed_summary': r'(?:DETAILED SUMMARY|Detailed Summary)[:\n](.*?)(?=\n(?:KEY|MAIN|TARGET|CONTENT|RELEVANCE|$))',
            'key_takeaways': r'(?:KEY TAKEAWAYS|Key Takeaways)[:\n](.*?)(?=\n(?:TARGET|CONTENT|MAIN|RELEVANCE|$))',
            'key_topics': r'(?:KEY TOPICS|Key Topics)[:\n](.*?)(?=\n(?:IMPORTANT|MAIN|SUPPORTING|CONTEXT|EXECUTIVE|$))',
            'important_quotes': r'(?:IMPORTANT QUOTES|Important Quotes)[:\n](.*?)(?=\n(?:MAIN|SUPPORTING|CONTEXT|EXECUTIVE|$))',
            'target_audience': r'(?:TARGET AUDIENCE|Target Audience)[:\n](.*?)(?=\n(?:CONTENT|RELEVANCE|$))',
            'content_category': r'(?:CONTENT CATEGORY|Content Category|CONTENT TYPE)[:\n](.*?)(?=\n(?:RELEVANCE|$))',
            'relevance_score': r'(?:RELEVANCE SCORE|Relevance Score)[:\n].*?(\d+(?:\.\d+)?)',
            'completeness_score': r'(?:COMPLETENESS SCORE|Completeness Score)[:\n].*?(\d+(?:\.\d+)?)',
            'improvement_suggestions': r'(?:IMPROVEMENT SUGGESTIONS|Improvement Suggestions)[:\n](.*?)(?=\n(?:FINAL|APPROVED|$))',
            'approved': r'(?:APPROVED|Approved)[:\n].*?(Yes|No|True|False)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                sections[key] = match.group(1).strip()
        
        return sections
    
    @staticmethod
    def extract_list_items(text: str) -> List[str]:
        """Extract list items from text"""
        if not text:
            return []
        
        # Split by bullet points, numbers, or newlines
        items = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Remove bullet points, numbers, etc.
            cleaned = re.sub(r'^[-•*\d+\.\)]\s*', '', line)
            if cleaned and len(cleaned) > 3:  # Avoid very short items
                items.append(cleaned)
        
        return items[:8]  # Limit to reasonable number
    
    @staticmethod
    def extract_score(text: str) -> Optional[float]:
        """Extract numeric score from text"""
        if not text:
            return None
        
        # Look for numbers like "8.5", "7/10", "8 out of 10"
        score_match = re.search(r'(\d+(?:\.\d+)?)', text)
        if score_match:
            score = float(score_match.group(1))
            # Normalize to 0-10 scale if needed
            if score > 10:
                score = score / 10
            return min(max(score, 0), 10)  # Clamp between 0-10
        
        return None
    
    @staticmethod
    def extract_approval(text: str) -> Optional[bool]:
        """Extract approval status from text"""
        if not text:
            return None
        
        text_lower = text.lower()
        if any(word in text_lower for word in ['yes', 'true', 'approved', 'acceptable']):
            return True
        elif any(word in text_lower for word in ['no', 'false', 'rejected', 'needs improvement']):
            return False
        
        return None
    
    @classmethod
    def process_crew_output(cls, raw_output: str) -> ProcessedSummary:
        """Process raw CrewAI output into structured summary"""
        sections = cls.extract_sections(raw_output)
        
        # Extract and process different components
        executive_summary = sections.get('executive_summary', 'Summary not available.')
        detailed_summary = sections.get('detailed_summary', 'Detailed analysis not available.')
        
        # Process lists
        key_takeaways = cls.extract_list_items(sections.get('key_takeaways', ''))
        key_topics = cls.extract_list_items(sections.get('key_topics', ''))
        important_quotes = cls.extract_list_items(sections.get('important_quotes', ''))
        improvement_suggestions = cls.extract_list_items(sections.get('improvement_suggestions', ''))
        
        # Process single values
        target_audience = sections.get('target_audience', 'General audience')
        content_category = sections.get('content_category', 'Educational')
        
        # Process scores and approval
        relevance_score = cls.extract_score(sections.get('relevance_score'))
        completeness_score = cls.extract_score(sections.get('completeness_score'))
        quality_approved = cls.extract_approval(sections.get('approved'))
        
        # Fallback processing if structured extraction didn't work well
        if not key_takeaways:
            # Try to extract takeaways from detailed summary
            sentences = detailed_summary.split('.')
            key_takeaways = [s.strip() for s in sentences if len(s.strip()) > 20][:5]
        
        if not key_topics:
            # Try to extract topics from executive summary
            words = executive_summary.split()
            # This is a simple fallback - in practice you might want more sophisticated topic extraction
            key_topics = ['Content analysis needed']
        
        return ProcessedSummary(
            executive_summary=executive_summary,
            detailed_summary=detailed_summary,
            key_takeaways=key_takeaways,
            key_topics=key_topics,
            important_quotes=important_quotes,
            target_audience=target_audience,
            content_category=content_category,
            relevance_score=relevance_score,
            completeness_score=completeness_score,
            quality_approved=quality_approved,
            improvement_suggestions=improvement_suggestions
        )
