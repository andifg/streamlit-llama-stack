# 🦙 Streamlit Ollama Chat

A simple Streamlit chat interface that connects directly to Ollama.

## 🚀 Features

- **Direct Ollama Integration**: No intermediate servers needed
- **Dynamic Model Loading**: Automatically detects and loads all available Ollama models
- **Temperature Control**: Adjust response creativity
- **Connection Testing**: Built-in health check
- **Model Discovery**: Automatically detect available models

## 📋 Prerequisites

- Python 3.9 or higher (excluding 3.9.7)
- [Poetry](https://python-poetry.org/) for dependency management
- [Ollama](https://ollama.ai/) installed and running

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

# Install dependencies with Poetry
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

## 🎯 Running the App

```bash
# Run the Streamlit app with Poetry
poetry run streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## ⚙️ Configuration

- **Ollama URL**: Default is `http://localhost:11434`
- **Model**: Automatically loads all models available in your Ollama installation
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
   - Check if port 11434 is available
   - Use "Test Connection" button in sidebar

2. **Model Not Found**:
   - Pull the model: `ollama pull llama3.2:3b`
   - Check available models: `ollama list`
   - Use "Refresh Models" button to see installed models

3. **Poetry Issues**:
   - Reinstall dependencies: `poetry install`
   - Clear cache: `poetry cache clear pypi --all`
   - Update Poetry: `poetry self update`

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
├── pyproject.toml     # Poetry configuration
├── app.py            # Main Streamlit application
├── README.md         # This file
└── .venv/            # Virtual environment (created by Poetry)
```

## 🔗 Useful Links

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📝 License

This project is open source and available under the MIT License. 