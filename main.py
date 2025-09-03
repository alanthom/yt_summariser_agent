"""
Main entry point for the YouTube Summarizer using CrewAI
"""
import sys
import os
from pathlib import Path

# Disable CrewAI telemetry early to prevent connection errors
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.summarizer import YouTubeSummarizer
from src.config import Config

def main():
    """Main function to run the YouTube Summarizer"""
    try:
        # Check if .env file exists
        if not os.path.exists('.env'):
            print("⚠️  No .env file found!")
            print("🔧 Setting up for first time use...")
            print("\nThis system uses Ollama (free open-source models)")
            print("Run the setup script first:")
            print("  python setup.py")
            print("\nOr create a .env file manually:")
            print("  OLLAMA_BASE_URL=http://localhost:11434")
            print("  OLLAMA_MODEL=llama3:8b")
            return
        
        # Validate configuration
        Config.validate()
        
        # Create and run summarizer
        summarizer = YouTubeSummarizer()
        
        # Check if URL provided as command line argument
        if len(sys.argv) > 1:
            url = sys.argv[1]
            print(f"🎯 Processing URL: {url}")
            summary = summarizer.summarize_video(url)
            if summary:
                summarizer.display_summary_preview(summary)
        else:
            # Run in interactive mode
            summarizer.run_interactive()
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure Ollama is running: ollama serve")
        print("2. Check available models: ollama list")
        print("3. Install a model: ollama pull llama3:8b")
        print("4. Run setup again: python setup.py")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n🔧 Try installing requirements:")
        print("  pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n🔧 Please check your configuration:")
        print("1. Ensure Ollama is installed and running")
        print("2. Verify your model is available")
        print("3. Run setup if needed: python setup.py")

if __name__ == "__main__":
    main()
