"""
Setup script for the YouTube Summarizer
"""
import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def setup_env_file():
    """Help user set up environment file"""
    if os.path.exists('.env'):
        print("✅ .env file already exists!")
        return True
    
    print("⚙️ Setting up environment file...")
    print("This system uses Ollama (free open-source models)")
    print("Default configuration will be created.")
    
    # Ask for custom model preference
    print("\nAvailable model options:")
    print("1. llama3:8b (Recommended - best quality)")
    print("2. llama3.2:3b (Faster processing)")
    print("3. mistral:7b (Alternative option)")
    print("4. Custom model name")
    
    choice = input("Choose model option (1-4) [1]: ").strip() or "1"
    
    model_map = {
        "1": "llama3:8b",
        "2": "llama3.2:3b", 
        "3": "mistral:7b"
    }
    
    if choice in model_map:
        model = model_map[choice]
    elif choice == "4":
        model = input("Enter custom model name: ").strip() or "llama3:8b"
    else:
        model = "llama3:8b"
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write(f"OLLAMA_BASE_URL=http://localhost:11434\n")
        f.write(f"OLLAMA_MODEL={model}\n")
        f.write("MODEL_TEMPERATURE=0.7\n")
        f.write("MAX_TOKENS=4000\n")
    
    print("✅ .env file created successfully!")
    print(f"📝 Model set to: {model}")
    return True

def check_ollama():
    """Check if Ollama is installed and running"""
    print("🔍 Checking Ollama installation...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("✅ Ollama is running!")
            if models:
                print(f"📦 Found {len(models)} installed models:")
                for model in models[:5]:  # Show first 5
                    print(f"   • {model['name']}")
            else:
                print("⚠️  No models installed yet")
            return True, models
        else:
            print("❌ Ollama is not responding")
            return False, []
    except ImportError:
        print("⚠️  requests package not installed yet")
        return False, []
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False, []

def install_ollama_model(model_name="llama3:8b"):
    """Help user install Ollama model"""
    print(f"\n🚀 Installing model: {model_name}")
    print("This may take several minutes depending on your internet connection...")
    
    try:
        result = subprocess.run([
            "ollama", "pull", model_name
        ], capture_output=True, text=True, timeout=600)  # 10 minute timeout
        
        if result.returncode == 0:
            print(f"✅ Model {model_name} installed successfully!")
            return True
        else:
            print(f"❌ Failed to install model: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⏱️  Installation timed out. Please try manually: ollama pull " + model_name)
        return False
    except FileNotFoundError:
        print("❌ Ollama command not found. Please install Ollama first.")
        print("   Download from: https://ollama.ai")
        return False
    except Exception as e:
        print(f"❌ Error installing model: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    os.makedirs("outputs", exist_ok=True)
    print("✅ Directories created!")

def main():
    """Main setup function"""
    print("🚀 YouTube Summarizer Setup (CrewAI + Open Source)")
    print("=" * 50)
    
    # Step 1: Install packages
    print("\n📦 STEP 1: Installing Python packages...")
    if not install_requirements():
        return
    
    # Step 2: Create directories
    print("\n📁 STEP 2: Creating directories...")
    create_directories()
    
    # Step 3: Check Ollama
    print("\n🤖 STEP 3: Checking Ollama...")
    ollama_running, models = check_ollama()
    
    if not ollama_running:
        print("\n❌ Ollama is not running or not installed")
        print("📋 Please follow these steps:")
        print("1. Download and install Ollama from: https://ollama.ai")
        print("2. Start Ollama: ollama serve")
        print("3. Run this setup again")
        return
    
    # Step 4: Setup environment
    print("\n⚙️  STEP 4: Setting up environment...")
    if not setup_env_file():
        return
    
    # Step 5: Check/install model
    print("\n🔍 STEP 5: Checking model availability...")
    
    # Read the model from .env file
    model_name = "llama3.2:latest"  # default
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('OLLAMA_MODEL='):
                    model_name = line.split('=')[1].strip()
                    break
    except:
        pass
    
    model_names = [m['name'] for m in models]
    if model_name not in model_names:
        print(f"⚠️  Model '{model_name}' not found")
        install_choice = input(f"Install {model_name}? (y/n) [y]: ").strip().lower()
        
        if install_choice in ['', 'y', 'yes']:
            if install_ollama_model(model_name):
                print(f"✅ Model {model_name} ready!")
            else:
                print(f"❌ Model installation failed")
                print(f"💡 Try manually: ollama pull {model_name}")
        else:
            print("⚠️  You'll need to install a model before using the summarizer")
    else:
        print(f"✅ Model '{model_name}' is already available!")
    
    print("\n🎉 Setup complete!")
    print("\n🚀 To run the summarizer:")
    print("  python main.py")
    print("\n🎯 Or with a direct URL:")
    print("  python main.py https://www.youtube.com/watch?v=VIDEO_ID")
    print("\n💡 Need help?")
    print("  • Check Ollama status: ollama list")
    print("  • Start Ollama: ollama serve")
    print("  • Install models: ollama pull llama3:8b")

if __name__ == "__main__":
    main()
