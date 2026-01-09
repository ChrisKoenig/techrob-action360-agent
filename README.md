# TechRob Action360 AI Agent

A flexible, multi-platform AI agent built with Microsoft Agent Framework that connects to MCP servers, uses Azure AI Foundry's GPT-4o model, and is accessible from Teams/M365 Copilot, web applications, and PowerBI.

## Features

- **Microsoft Agent Framework**: Flexible agent orchestration and execution
- **MCP Server Integration**: Connect to Model Context Protocol servers for data retrieval
- **Azure AI Foundry GPT-4o**: Leverages the latest GPT-4o model from Microsoft Foundry
- **Multi-Platform Deployment**: 
  - M365 Copilot / Teams integration
  - REST API for web applications
  - PowerBI custom function support
  - Direct programmatic access

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── agent.py                 # Core agent implementation
│   ├── mcp_handler.py           # MCP server connection handler
│   ├── api.py                   # REST API for multi-platform access
│   └── models/
│       └── config.py            # Configuration models
├── config/
│   ├── agent_config.yaml        # Agent configuration
│   └── mcp_tools.yaml           # MCP tools configuration
├── tests/
│   ├── __init__.py
│   └── test_agent.py            # Agent tests
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Prerequisites

- Python 3.10+
- Microsoft Foundry (formerly Azure AI Foundry) project with GPT-4o model deployed
- MCP server running (local or remote)
- Azure subscription with appropriate credentials

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd c:\src\techrob_action360_agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   > **Note:** The `--pre` flag may be required for preview versions:
   > ```bash
   > pip install agent-framework-azure-ai --pre
   > ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Foundry credentials and MCP server details
   ```

## Configuration

### Environment Variables (.env)

- `FOUNDRY_PROJECT_NAME`: Your Microsoft Foundry project name
- `FOUNDRY_RESOURCE_GROUP`: Azure resource group
- `FOUNDRY_SUBSCRIPTION_ID`: Azure subscription ID
- `MODEL_NAME`: Model name (e.g., gpt-4o)
- `MODEL_DEPLOYMENT`: Model deployment name
- `MCP_SERVER_URL`: MCP server endpoint
- `API_PORT`: Port for REST API
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

### Agent Configuration

Edit `config/agent_config.yaml` to customize:
- Agent name and description
- System prompt
- Tool definitions
- Response formatting

## Quick Start

### Running the Agent

```bash
python -m src.agent
```

### Starting the REST API

```bash
python -m src.api
```

The API will be available at `http://localhost:8000`

### Example: Chat with the Agent

```python
from src.agent import TechRobAgent
import asyncio

async def main():
    agent = TechRobAgent()
    response = await agent.process_query("What data is available?")
    print(response)

asyncio.run(main())
```

## Multi-Platform Integration

### Teams/M365 Copilot
1. Configure the REST API endpoint in Teams manifest
2. Register as a custom plugin/skill
3. Agent will be accessible in Teams conversations

### Web Application
Call the REST API endpoint:
```javascript
const response = await fetch('http://localhost:8000/api/query', {
  method: 'POST',
  body: JSON.stringify({ query: 'Your question here' })
});
```

### PowerBI
Create a custom function or R/Python script that calls the agent API

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Lint code
pylint src/

# Type checking
mypy src/
```

## API Endpoints

- `POST /api/query` - Send a query to the agent
- `GET /api/health` - Health check
- `GET /api/tools` - List available tools from MCP server

## Troubleshooting

- **MCP Connection Issues**: Verify MCP server is running and URL is correct
- **Foundry Authentication**: Check Azure credentials in .env
- **API Port in Use**: Change `API_PORT` in .env

## Contributing

Follow PEP 8 style guidelines and include tests for new features.

## License

MIT License - see LICENSE file for details
