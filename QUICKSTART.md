# 🚀 Quick Start Guide

## Prerequisites

1. **Install Ollama** (Required - Free AI models)
   - Download from [ollama.ai](https://ollama.ai)
   - Install and start: `ollama serve`

2. **Python 3.8+** with pip

## Setup (30 seconds)

1. **Run the automated setup:**
   ```bash
   python setup.py
   ```
   This will:
   - Install Python dependencies
   - Set up configuration
   - Help you install an AI model
   - Check system readiness

2. **Alternative manual setup:**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Install AI model
   ollama pull llama3:8b
   
   # Create config
   copy .env.example .env
   ```

## Usage

### Interactive Mode (Recommended)
```bash
python main.py
```
Then paste any YouTube URL when prompted!

### Direct URL Processing
```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Batch Processing
```bash
python example.py
```

## Models

Choose your AI model based on your needs:

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `llama3.2:3b` | Small | Fast | Good | Quick summaries |
| `llama3:8b` | Medium | Balanced | Excellent | **Recommended** |
| `mistral:7b` | Medium | Fast | Very Good | Alternative option |

Change models in your `.env` file:
```
OLLAMA_MODEL=llama3:8b
```

## Troubleshooting

### "Cannot connect to Ollama"
```bash
ollama serve
```

### "Model not found"
```bash
ollama pull llama3:8b
```

### "No transcript available"
- Video might not have captions
- Try a different video
- Check if video is public

### Performance Issues
- Use a smaller model: `llama3.2:3b`
- Ensure sufficient RAM (8GB+ recommended)
- Close other applications

## Output

The system creates:
- **Markdown files**: Human-readable summaries
- **JSON files**: Structured data
- **Console preview**: Immediate results

Files are saved in the `outputs/` directory.

## System Requirements

- **RAM**: 8GB+ (for llama3:8b)
- **Storage**: 4-6GB for AI model
- **Internet**: Only for downloading models initially

## What Makes This Special?

✅ **100% Free** - No API keys or subscriptions  
✅ **Privacy First** - Everything runs locally  
✅ **Multi-Agent AI** - Three AI agents collaborate  
✅ **Professional Quality** - Production-ready summaries  
✅ **Easy Setup** - Just run setup.py  

## Need Help?

1. Run system check: `python example.py` → Option 4
2. Check Ollama: `ollama list`
3. Reinstall model: `ollama pull llama3:8b`
4. Run setup again: `python setup.py`

Happy summarizing! 🎬✨
