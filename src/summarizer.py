"""
YouTube Summarizer using CrewAI and Open Source Models
"""
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

from crewai import Crew

from src.config import Config
from src.models import VideoMetadata, FinalSummary, CrewOutput
from src.agents import (
    create_listener_agent,
    create_content_writer_agent,
    create_critic_agent,
    create_listener_task,
    create_content_writer_task,
    create_critic_task
)
from src.utils import YouTubeExtractor, FileManager, CrewOutputProcessor

class YouTubeSummarizer:
    """Main orchestrator for the YouTube summarization system using CrewAI"""
    
    def __init__(self):
        self.console = Console()

        # Validate configuration
        Config.validate()

        # Use local Ollama with codestral model
        provider = "ollama"
        self.console.print(f"🚀 Using provider: [bold green]Ollama[/bold green] (Local processing)")
        self.console.print(f"🤖 Model: [bold green]codestral:latest[/bold green]")
        
    def create_crew(self, transcript: str, metadata: dict):
        """Create the CrewAI crew with agents and tasks"""
        
        # Create agents
        listener_agent = create_listener_agent()
        content_writer_agent = create_content_writer_agent()
        critic_agent = create_critic_agent()
        
        # Create tasks
        listener_task = create_listener_task(transcript, metadata)
        content_writer_task = create_content_writer_task()
        critic_task = create_critic_task()
        
        # Assign agents to tasks
        listener_task.agent = listener_agent
        content_writer_task.agent = content_writer_agent
        critic_task.agent = critic_agent
        
        # Create crew
        crew = Crew(
            agents=[listener_agent, content_writer_agent, critic_agent],
            tasks=[listener_task, content_writer_task, critic_task],
            verbose=Config.CREW_VERBOSE,
            memory=Config.CREW_MEMORY
        )
        
        return crew
    
    def summarize_video(self, youtube_url: str) -> Optional[FinalSummary]:
        """Main method to summarize a YouTube video using CrewAI"""
        
        self.console.print(Panel.fit(
            "🎥 YouTube Video Summarizer (CrewAI + Open Source)",
            style="bold blue"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True,
        ) as progress:
            
            # Step 1: Extract video data
            task1 = progress.add_task("Extracting video metadata and transcript...", total=None)
            metadata, transcript = YouTubeExtractor.process_youtube_url(youtube_url)
            
            if not metadata or not transcript:
                self.console.print("[red]❌ Failed to extract video data[/red]")
                return None
            
            progress.update(task1, description="✅ Video data extracted")
            progress.stop_task(task1)
            
            self.console.print(f"📺 [bold]Video:[/bold] {metadata['title']}")
            self.console.print(f"📺 [bold]Channel:[/bold] {metadata.get('channel', 'Unknown')}")
            self.console.print(f"📝 [bold]Transcript length:[/bold] {len(transcript)} characters")
            self.console.print(f"🤖 [bold]Model:[/bold] {Config.OLLAMA_MODEL}\n")
            
            # Create video metadata object
            video_meta = VideoMetadata(**metadata)
            
            # Step 2: Create and run CrewAI crew
            task2 = progress.add_task("🚀 Creating AI crew...", total=None)
            
            try:
                crew = self.create_crew(transcript, metadata)
                progress.update(task2, description="✅ Crew created, starting collaboration...")
                
                # Execute the crew with timeout for testing
                self.console.print("🤖 [yellow]AI agents are collaborating...[/yellow]")
                self.console.print("   🎧 Listener Agent analyzing content...")
                self.console.print("   ✍️ Content Writer crafting summary...")
                self.console.print("   🔍 Critic Agent validating quality...")
                
                # Add timeout for testing - limit to 30 seconds (cross-platform)
                import threading
                import time
                
                result = None
                exception = None
                
                def run_crew():
                    nonlocal result, exception
                    try:
                        result = crew.kickoff()
                    except Exception as e:
                        exception = e
                
                # Start crew execution in separate thread
                crew_thread = threading.Thread(target=run_crew)
                crew_thread.daemon = True
                crew_thread.start()
                
                # Wait for completion or timeout
                crew_thread.join(timeout=180)  # Increase to 3 minutes for comprehensive processing
                
                if crew_thread.is_alive():
                    raise Exception("Processing timed out after 180 seconds - stopping for testing")
                
                if exception:
                    raise exception
                
                if result is None:
                    raise Exception("No result returned from crew execution")
                
                progress.update(task2, description="✅ AI collaboration completed")
                progress.stop_task(task2)
                
            except Exception as e:
                progress.stop_task(task2)
                self.console.print(f"[red]❌ CrewAI execution failed: {str(e)}[/red]")
                self.console.print("[yellow]💡 Troubleshooting tips:[/yellow]")
                self.console.print("   • Ensure Ollama is running: `ollama serve`")
                self.console.print(f"   • Check if model is available: `ollama list`")
                self.console.print(f"   • Pull model if needed: `ollama pull {Config.OLLAMA_MODEL}`")
                return None
            
            # Step 3: Process results
            task3 = progress.add_task("� Processing results...", total=None)
            
            # Create crew output object
            crew_output = CrewOutput(raw_output=str(result))
            
            # Process the output into structured format
            processed_summary = CrewOutputProcessor.process_crew_output(str(result))
            
            progress.update(task3, description="✅ Results processed")
            progress.stop_task(task3)
            
            # Step 4: Compile Final Summary
            final_summary = FinalSummary(
                video_metadata=video_meta,
                crew_output=crew_output,
                processed_summary=processed_summary
            )
            
            # Save final outputs
            json_path, md_path = FileManager.save_summary(final_summary)
            
            # Display success info
            self.console.print("\n🎉 [green]Processing Complete![/green]")
            self.console.print(f"📄 [bold]Summary saved to:[/bold]")
            self.console.print(f"   • JSON: {json_path}")
            self.console.print(f"   • Markdown: {md_path}")
            
            # Display quality metrics if available
            if processed_summary.relevance_score:
                self.console.print(f"📊 [bold]Quality Scores:[/bold]")
                self.console.print(f"   • Relevance: {processed_summary.relevance_score}/10")
                if processed_summary.completeness_score:
                    self.console.print(f"   • Completeness: {processed_summary.completeness_score}/10")
                if processed_summary.quality_approved is not None:
                    status = "✅ Approved" if processed_summary.quality_approved else "⚠️ Needs Review"
                    self.console.print(f"   • Status: {status}")
            
            return final_summary
    
    def display_summary_preview(self, summary: FinalSummary):
        """Display a preview of the generated summary"""
        self.console.print("\n" + "="*80)
        self.console.print("[bold blue]EXECUTIVE SUMMARY PREVIEW[/bold blue]")
        self.console.print("="*80)
        
        # Executive summary
        self.console.print(summary.processed_summary.executive_summary)
        
        # Key takeaways
        if summary.processed_summary.key_takeaways:
            self.console.print("\n[bold blue]KEY TAKEAWAYS[/bold blue]")
            for i, takeaway in enumerate(summary.processed_summary.key_takeaways, 1):
                self.console.print(f"{i}. {takeaway}")
        
        # Quality scores
        if summary.processed_summary.relevance_score or summary.processed_summary.completeness_score:
            self.console.print(f"\n[bold blue]QUALITY ASSESSMENT[/bold blue]")
            if summary.processed_summary.relevance_score:
                self.console.print(f"Relevance: {summary.processed_summary.relevance_score}/10")
            if summary.processed_summary.completeness_score:
                self.console.print(f"Completeness: {summary.processed_summary.completeness_score}/10")
        
        # Target audience
        self.console.print(f"\n[bold blue]TARGET AUDIENCE[/bold blue]")
        self.console.print(summary.processed_summary.target_audience)
        
        self.console.print("\n" + "="*80)
    
    def check_ollama_status(self):
        """Check if Ollama is running and models are available"""
        try:
            available_models = Config.get_available_models()
            if available_models:
                self.console.print(f"✅ [green]Ollama is running[/green]")
                self.console.print(f"📦 [bold]Available models:[/bold] {', '.join(available_models)}")
                if Config.OLLAMA_MODEL in available_models:
                    self.console.print(f"🎯 [green]Target model '{Config.OLLAMA_MODEL}' is ready[/green]")
                else:
                    self.console.print(f"⚠️ [yellow]Target model '{Config.OLLAMA_MODEL}' not found[/yellow]")
                    self.console.print(f"💡 Install it with: [dim]ollama pull {Config.OLLAMA_MODEL}[/dim]")
            else:
                self.console.print("❌ [red]No models found in Ollama[/red]")
        except Exception as e:
            self.console.print(f"❌ [red]Ollama connection failed: {str(e)}[/red]")
            self.console.print("💡 [yellow]Start Ollama with: [dim]ollama serve[/dim][/yellow]")
    
    def run_interactive(self):
        """Run the summarizer in interactive mode"""
        self.console.print(Panel.fit(
            "Welcome to the YouTube Video Summarizer!\n"
            "Powered by CrewAI and Open Source Models 🚀\n\n"
            "This system uses three AI agents working together:\n"
            "• 🎧 Listener Agent: Extracts key insights from content\n"
            "• ✍️ Content Writer: Crafts polished, engaging summaries\n"
            "• 🔍 Critic Agent: Validates quality and provides feedback\n\n"
            "✨ 100% Free - No API keys required!\n"
            "Just paste a YouTube URL to get started!",
            title="🤖 AI-Powered YouTube Summarizer",
            style="cyan"
        ))
        
        # Check Ollama status
        self.check_ollama_status()
        
        while True:
            try:
                url = self.console.input("\n[bold]Enter YouTube URL (or 'quit' to exit): [/bold]")
                
                if url.lower() in ['quit', 'exit', 'q']:
                    self.console.print("[yellow]👋 Goodbye![/yellow]")
                    break
                
                if not url.strip():
                    continue
                
                # Process the video
                summary = self.summarize_video(url.strip())
                
                if summary:
                    # Show preview
                    show_preview = self.console.input("\n[bold]Show summary preview? (y/n): [/bold]").lower()
                    if show_preview.startswith('y'):
                        self.display_summary_preview(summary)
                
                # Ask if user wants to continue
                continue_choice = self.console.input("\n[bold]Process another video? (y/n): [/bold]").lower()
                if not continue_choice.startswith('y'):
                    self.console.print("[yellow]👋 Goodbye![/yellow]")
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]❌ Error: {str(e)}[/red]")
                self.console.print("🔧 [yellow]Try checking your Ollama installation and model availability[/yellow]")
                continue
