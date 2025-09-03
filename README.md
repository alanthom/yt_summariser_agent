
# YouTube Channel Summarizer (CrewAI + Open Source)

An intelligent multi-agent system using **CrewAI** and **open-source models** to summarize YouTube videos with three specialized agents:

- **Listener Agent**: Expert at capturing the crux and key pointers from video content
- **Content Writer Agent**: Proficient at crafting high-quality summaries and content
- **Critic Agent**: Cross-verifies information relevance and accuracy

## 🚀 Features

- **100% Free**: Uses open-source models via Ollama (no API keys required!)
- **CrewAI Framework**: Advanced multi-agent collaboration
- **Local Processing**: All AI processing happens locally on your machine
- **Rich Output**: Beautiful console interface with progress tracking
- **Multiple Formats**: Saves summaries in JSON and Markdown

## 📋 Prerequisites

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Python 3.8+**: Make sure Python is installed

## 🛠️ Setup

### 1. Install Ollama and Model
```bash
# Download and install Ollama from https://ollama.ai
# Then pull a model (we recommend llama3:8b for best results)
ollama pull llama3:8b

# Or use a lighter model for faster processing
ollama pull llama3.2:3b
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env to set your model preference (default is llama3:8b)
```

### 4. Run the Summarizer
```bash
python main.py
```

## 🎯 Usage

### Interactive Mode
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

## 🤖 Available Models

The system works with any Ollama model. Recommended options:

- **llama3:8b** - Best quality, slower processing
- **llama3.2:3b** - Good quality, faster processing  
- **mistral:7b** - Alternative high-quality option
- **codellama:7b** - Good for technical content

Change models by editing the `OLLAMA_MODEL` in your `.env` file.

## 📁 Output

The system generates:
- **JSON files**: Structured data with all agent outputs
- **Markdown files**: Human-readable summaries
- **Console preview**: Immediate results display

All outputs are saved in the `outputs/` directory.

## 🔧 Troubleshooting

**Model not found?**
```bash
ollama list  # Check installed models
ollama pull llama3:8b  # Install recommended model
```

**Ollama not running?**
```bash
ollama serve  # Start Ollama server
```

**Connection issues?**
- Check if Ollama is running on localhost:11434
- Verify your model is pulled and available

## 🎨 Architecture

```
YouTube URL → Transcript Extraction → CrewAI Agents → Final Summary
                                           ↓
                ┌─────────────────────────────────────────────┐
                │  🎧 Listener Agent                          │
                │  (Extracts key insights & important points)  │
                └─────────────────────────────────────────────┘
                                           ↓
                ┌─────────────────────────────────────────────┐
                │  ✍️ Content Writer Agent                    │
                │  (Crafts polished summaries & takeaways)    │
                └─────────────────────────────────────────────┘
                                           ↓
                ┌─────────────────────────────────────────────┐
                │  🔍 Critic Agent                            │
                │  (Validates quality & relevance)            │
                └─────────────────────────────────────────────┘
```
>>>>>>> master
