# 🦙 Streamlit Ollama Chat

A simple Streamlit chat interface that connects directly to Ollama.

## 🚀 Features

- **Llama Stack Integration**: Uses Llama Stack client for model discovery
- **Dynamic Model Loading**: Automatically detects and loads all available inference models
- **Hybrid Architecture**: Llama Stack for models, Ollama for chat generation
- **Temperature Control**: Adjust response creativity
- **Connection Testing**: Built-in health check for both services
- **Model Discovery**: Automatically detect available models

## 📋 Prerequisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- [Ollama](https://ollama.ai/) installed and running
- [Llama Stack](https://github.com/meta-llama/llama-stack) server running

## 🛠️ Installation & Setup

### 1. Install Poetry (if not already installed)

```bash
# On macOS/Linux:
curl -sSL https://install.python-poetry.org | python3 -

# On Windows (PowerShell):
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Or via pip:
pip install poetry
```

### 2. Setup Project

```bash
# Clone or navigate to your project directory
cd streamlit-ollama-chat

# Install dependencies with Poetry (including llama-stack-client)
poetry install

# Activate the virtual environment
poetry shell
```

### 3. Install and Setup Ollama

```bash
# Install Ollama
# On macOS:
brew install ollama

# On Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# On Windows: Download from https://ollama.ai/download/windows
```

```bash
# Start Ollama service (runs on port 11434 by default)
ollama serve

# In another terminal, pull a model
ollama pull llama3.2:3b

# Check available models
ollama list
```

### 4. Install and Setup Llama Stack

```bash
# Install Llama Stack
pip install llama-stack

# Configure Llama Stack to use Ollama
llama stack configure

# Start Llama Stack server (runs on port 8321 by default)
llama stack run --port 8321
```

## 🎯 Running the App

```bash
# Run the Streamlit app with Poetry
poetry run streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## ⚙️ Configuration

- **Llama Stack URL**: Default is `http://localhost:8321` (for model discovery)
- **Ollama URL**: Default is `http://localhost:11434` (for chat generation)
- **Model**: Automatically loads all inference models available via Llama Stack
- **Temperature**: Control response randomness (0.0 = deterministic, 1.0 = creative)
- **Auto-refresh**: Models are cached for 30 seconds and can be manually refreshed

## 🔧 Available Commands

```bash
# Install dependencies
poetry install

# Add a new dependency
poetry add package-name

# Add development dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Show dependency tree
poetry show --tree

# Run commands in Poetry environment
poetry run streamlit run app.py

# Activate shell
poetry shell

# Build package
poetry build
```

## 🐛 Troubleshooting

### Common Issues:

1. **Connection Error**:
   - Ensure Ollama is running: `ollama serve`
   - Ensure Llama Stack is running: `llama stack run --port 8321`
   - Check if ports 11434 (Ollama) and 8321 (Llama Stack) are available
   - Use "Test Connection" button in sidebar

2. **Model Not Found**:
   - Pull models in Ollama: `ollama pull llama3.2:3b`
   - Check available models: `ollama list`
   - Ensure Llama Stack is configured to use Ollama
   - Use "Refresh Models" button to reload from Llama Stack

3. **Poetry Issues**:
   - Reinstall dependencies: `poetry install`
   - Clear cache: `poetry cache clear pypi --all`
   - Update Poetry: `poetry self update`

4. **Llama Stack Issues**:
   - Check Llama Stack configuration: `llama stack configure`
   - Verify Ollama integration in Llama Stack
   - Check Llama Stack logs for errors

## 📦 Recommended Models

```bash
# Small and fast
ollama pull llama3.2:3b

# Larger and more capable
ollama pull llama3.1:8b

# Code-specific
ollama pull codellama:7b

# Alternative model
ollama pull mistral:7b
```

## 📁 Project Structure

```
streamlit-ollama-chat/
├── pyproject.toml          # Poetry configuration
├── app.py                  # Main Streamlit application
├── llama_stack_service.py  # Llama Stack service integration
├── README.md               # This file
├── .gitignore              # Git ignore patterns
└── .venv/                  # Virtual environment (created by Poetry)
```

## 🔗 Useful Links

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📝 License

This project is open source and available under the MIT License. 