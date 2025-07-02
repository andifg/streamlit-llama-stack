# 🦙 Streamlit LlamaStack

A modern Streamlit chat interface for Llama Stack models.

## 🚀 Features

- **Web-Search Powered ReActAgent**: Uses llama-stack-client ReActAgent with integrated web search capabilities via Tavily API
- **Real-Time Information Access**: Get current, up-to-date information through web search integration
- **Dynamic Model Loading**: Automatically detects and loads all available inference models
- **Clean Package Structure**: Organized as a proper Python package
- **ReActAgent Session Management**: Maintains conversation context across turns
- **Temperature Control**: Adjust response creativity
- **Connection Testing**: Built-in health check for Llama Stack
- **Model Discovery**: Automatically detect available models
- **Easy CLI Access**: Run with `uv run streamlit-llamastack`

> **Web-Search Enhanced ReAct Pattern**: This app uses a specialized ReActAgent configured as a web search assistant that can look up current information and provide real-time, fact-based responses using the Tavily search API.

## 📋 Prerequisites

- Python 3.12 or higher
- `make` (usually pre-installed on macOS/Linux)
- [uv](https://docs.astral.sh/uv/) for dependency management (fast Python package installer)
- [Ollama](https://ollama.ai/) installed and running
- [Llama Stack](https://github.com/meta-llama/llama-stack) server running
- **[Tavily API Key](https://tavily.com/)** for web search functionality

## 🚀 Quick Start

> **🚀 Integrated Llama Stack Server**: This project now includes the Llama Stack server and can start it automatically. The Streamlit app connects to the integrated Llama Stack instance running on `http://localhost:8321`.

### 1. Install Prerequisites

```bash
# Install uv (much faster than pip and poetry)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Ollama (macOS)
brew install ollama
# OR Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Install Llama Stack
uv tool install llama-stack
```

### 2. Setup Project

```bash
# Install dependencies with uv
uv sync

# Install dev dependencies too
uv sync --extra dev

# Set up Tavily API key for web search
export TAVILY_SEARCH_API_KEY="your_tavily_api_key_here"
# Or add to your .bashrc/.zshrc for persistence
```

> **🔑 Get your Tavily API key**: Sign up at [tavily.com](https://tavily.com/) to get your free API key for web search functionality.

### 3. Start Services

```bash
# Start Ollama (managed by this setup)
ollama serve

# Pull a model for Ollama
ollama pull llama3.2:3b

# Start the integrated Llama Stack server
INFERENCE_MODEL=llama3.2:3b uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

> **💡 Pro Tip**: The Llama Stack server will automatically start with the specified model and run on `http://localhost:8321`. Keep this running in a separate terminal while using the Streamlit app.


### 4. Run the App

```bash
# Run the Streamlit app with the uv script
uv run streamlit-llamastack

# Or alternatively, run directly with streamlit
uv run streamlit run streamlit_llamastack/app.py
```

The app will open in your browser at `http://localhost:8501`.

> **🔄 Two Terminal Setup**: You'll need two terminal windows:
> 1. **Terminal 1**: Running the Llama Stack server (step 3)
> 2. **Terminal 2**: Running the Streamlit app (step 4)

### 🔍 **What can you ask the Web-Search Agent?**

The ReActAgent is now configured to search the web for current information. Try questions like:
- "What's the latest news about AI developments?"
- "What's the current stock price of Tesla?"
- "What's the weather like in Tokyo today?"
- "What are the latest developments in quantum computing?"
- "Who won the latest sports championship?"

## ⚙️ Configuration

- **Llama Stack URL**: Default is `http://localhost:8321` (for model discovery and ReActAgent chat)
- **Model**: Automatically loads all inference models available via Llama Stack
- **Temperature**: Control response randomness (0.0 = deterministic, 1.0 = creative)
- **Web Search**: Powered by Tavily API - requires `TAVILY_SEARCH_API_KEY` environment variable
- **ReActAgent Role**: Configured as a web search assistant that must use web search for current information
- **ReActAgent Sessions**: Each conversation maintains context through ReActAgent sessions
- **Auto-refresh**: Models are cached for 30 seconds and can be manually refreshed
- **Session Reset**: Clear chat history and reset ReActAgent session for fresh conversations
- **Integrated Server**: Llama Stack server is now part of the project


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

# Note: All commands automatically use uv to run tools
```

## 🐛 Troubleshooting

### Common Issues:

1. **Connection Error**:
   - Ensure Ollama is running: `ollama serve`
   - Ensure Llama Stack server is running: `INFERENCE_MODEL=llama3.2:3b uv run --with llama-stack llama stack build --template ollama --image-type venv --run`
   - Check if ports 11434 (Ollama) and 8321 (Llama Stack) are available
   - Use "Test Connection" button in sidebar

2. **Web Search Not Working**:
   - Verify `TAVILY_SEARCH_API_KEY` environment variable is set
   - Check Tavily API key is valid: `echo $TAVILY_SEARCH_API_KEY`
   - Ensure Llama Stack has web search provider configured
   - Check for network connectivity issues

3. **Model Not Found**:
   - Pull models in Ollama: `ollama pull llama3.2:3b`
   - Check available models: `ollama list`
   - Ensure Llama Stack is configured to use Ollama
   - Use "Refresh Models" button to reload from Llama Stack

4. **uv Issues**:
   - Reinstall dependencies: `uv sync`
   - Clear cache: `uv cache clean`
   - Update uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

5. **Llama Stack Issues**:
   - Check Llama Stack configuration: `llama stack configure`
   - Verify Ollama integration in Llama Stack
   - Check Llama Stack logs for errors
   - **Build failures**: Install system dependencies: `brew install pkg-config cmake coreutils` (macOS) or `sudo apt-get install pkg-config cmake` (Ubuntu)
   - **Server startup**: Ensure you're using the correct command: `INFERENCE_MODEL=llama3.2:3b uv run --with llama-stack llama stack build --template ollama --image-type venv --run`

## 🚀 Integrated Llama Stack Server

This project now includes the Llama Stack server as part of the setup. The server is started using uv and runs on `http://localhost:8321`.

### Starting the Server

```bash
# Start the integrated Llama Stack server with a specific model
INFERENCE_MODEL=llama3.2:3b uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

### Server Features

- **Automatic Model Loading**: The server automatically loads the specified model from Ollama
- **ReActAgent Support**: Full support for ReActAgent with web search capabilities
- **Template-based**: Uses the Ollama template for seamless integration
- **Environment Isolation**: Runs in its own virtual environment via uv

### Using Different Models

You can change the model by modifying the `INFERENCE_MODEL` environment variable:

```bash
# Use a different model
INFERENCE_MODEL=llama3.1:8b uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

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
streamlit-llama-stack/
├── streamlit_llamastack/   # Main package directory
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # CLI entry point
│   ├── app.py             # Main Streamlit application
│   └── service.py         # Llama Stack service integration
├── pyproject.toml         # uv/PEP 621 configuration with scripts
├── uv.lock                # Lockfile for reproducible builds
├── README.md              # This file
├── .gitignore             # Git ignore patterns
└── .venv/                 # Virtual environment (created by uv)
```

## 🔗 Useful Links

- [uv Documentation](https://docs.astral.sh/uv/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📝 License

This project is open source and available under the MIT License. 