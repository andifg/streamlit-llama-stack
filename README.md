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
- `make` (usually pre-installed on macOS/Linux)
- [Poetry](https://python-poetry.org/) for dependency management
- [Ollama](https://ollama.ai/) installed and running
- [Llama Stack](https://github.com/meta-llama/llama-stack) server running

## 🚀 Quick Start

### 1. Install Prerequisites

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install Ollama (macOS)
brew install ollama
# OR Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Install Llama Stack
pip install llama-stack
```

### 2. Setup Project

```bash
# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

### 3. Start Services

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Pull a model and start Llama Stack
ollama pull llama3.2:3b
llama stack run --port 8321
```

### 4. Run the App

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


## 🧹 Code Quality Tools

This project includes automated code quality tools to maintain consistent code standards:

### Quality Tools Included:
- **black**: Code formatting (line length 88, Python 3.12 target)
- **isort**: Import organization (black-compatible profile)
- **mypy**: Type checking with strict configuration

### Using Makefile Commands:

```bash
# Format code with black
make format

# Sort imports with isort
make sort-imports

# Run type checking with mypy
make type-check

# Run all quality checks
make quality-check

# Fix all quality issues (format + sort imports)
make quality-fix

# Show available commands
make help
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