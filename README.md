# TechRob Action360 AI Agent

A production-ready AI agent built with Microsoft Agent Framework that intelligently routes Azure DevOps Actions using GPT-4o from Azure AI Foundry. Features dynamic instruction sets, full MCP integration with Azure DevOps, and multi-platform REST API access.

## Features

- **Smart Action Routing**: Analyzes Actions through a 7-phase deterministic routing engine
- **Dynamic Instructions**: Switch between summary and routing modes without restarting
- **Azure DevOps MCP Integration**: Full access to work items, PRs, pipelines, and team capacity
- **Microsoft Agent Framework**: Flexible agent orchestration with Azure AI Foundry GPT-4o
- **Multi-Platform Access**: 
  - REST API with streaming support (Server-Sent Events)
  - PowerShell scripts for command-line access
  - Python async/await interface
  - Direct programmatic access

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── agent.py                 # Core agent with dynamic instructions & MCP
│   ├── api.py                   # REST API (query, streaming, health, tools)
│   └── models/
│       └── config.py            # Configuration models
├── config/
│   ├── instructions_summary.md  # Summary instruction set (default)
│   ├── instructions_routing.md  # Routing instruction set (7 phases)
│   └── instructions.md          # Legacy default instructions
├── tests/
│   └── test_agent.py            # Unit tests
├── logs/
│   └── agent.log                # Auto-cleared on each startup
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # Python dependencies
├── run_api.py                   # REST API server launcher
├── routing.ps1                  # PowerShell script for routing queries
├── query.ps1                    # PowerShell script for summary queries
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Prerequisites

- Python 3.10+
- Azure subscription with Foundry project containing GPT-4o deployment
- Azure CLI (`az` command) for authentication
- Node.js 16+ (for Azure DevOps MCP server)
- Azure DevOps organization (optional, for MCP integration)

## Getting Started

For a quick 5-minute setup, see [QUICKSTART.md](QUICKSTART.md).
For detailed routing analysis capabilities, see [Routing Instructions](config/instructions_routing.md).

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ChrisKoenig/techrob-action360-agent.git
   cd techrob-action360-agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate          # Windows
   # source venv/bin/activate       # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure credentials (see below)
   ```

## Configuration

### Environment Variables (.env)

**Azure AI Foundry:**
- `FOUNDRY_PROJECT_ENDPOINT`: Your Foundry project endpoint (e.g., `https://eastus.api.azureml.ms`)
- `FOUNDRY_PROJECT_NAME`: Foundry project name
- `FOUNDRY_RESOURCE_GROUP`: Azure resource group
- `FOUNDRY_SUBSCRIPTION_ID`: Azure subscription ID
- `MODEL_DEPLOYMENT`: Deployed model name (default: `gpt-4o`)

**Azure DevOps MCP:**
- `ADO_ORG_NAME`: Azure DevOps organization name (default: `UnifiedActionTracker`)
- `ADO_PROJECT_NAME`: Azure DevOps project name (default: `Unified Action Tracker`)

**API & Logging:**
- `API_PORT`: REST API port (default: `8000`)
- `API_HOST`: API host (default: `0.0.0.0`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## Running the Agent

### REST API Server

```bash
python run_api.py
```

Server starts at `http://localhost:8000`. Logs are written to `logs/agent.log` (auto-cleared on startup).

### Using PowerShell Scripts

For routing analysis:
```powershell
.\routing.ps1 676893
```

For summary/lookup:
```powershell
.\query.ps1 "Show me action 12345"
```

## API Endpoints

### POST /api/query
Analyze an Action with specified instruction type:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze action 676893", "instruction_type": "routing"}'
```

### POST /api/query/stream
Stream response as Server-Sent Events:
```bash
curl -X POST http://localhost:8000/api/query/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze action 676893", "instruction_type": "routing"}'
```

### GET /api/health
Health check:
```bash
curl http://localhost:8000/api/health
```

### GET /api/tools
List available tools and instruction types:
```bash
curl http://localhost:8000/api/tools
```

## Using in Python

```python
import asyncio
from src.agent import TechRobAgent

async def main():
    # Summary mode (default)
    agent = TechRobAgent(instruction_type="summary")
    await agent.initialize()
    response = await agent.process_query("Show action 676893")
    print(response)
    
    # Switch to routing mode
    agent.set_instruction_type("routing")
    routing = await agent.process_query("Analyze action 676893 for routing")
    print(routing)
    
    await agent.cleanup()

asyncio.run(main())
```

## Instruction Sets

The agent supports different instruction modes:

- **`summary`** (default): Quick lookups and information retrieval
- **`routing`**: Comprehensive 7-phase routing analysis for Actions

See [DYNAMIC_INSTRUCTIONS.md](DYNAMIC_INSTRUCTIONS.md) for details.

## MCP Integration

The agent automatically connects to Azure DevOps via MCP and has access to:
- Work items (fetch, create, update)
- Pull requests
- Pipelines and builds
- Team capacity and iterations
- Repository management

The MCP server is launched automatically when the agent initializes. Ensure the Azure DevOps organization and project names are set in `.env`.

## Testing

Run unit tests:
```bash
pytest tests/
```

## Troubleshooting

### Authentication Error
```bash
az login
```

### Port Already in Use
Change `API_PORT` in `.env` (e.g., to `8001`).

### MCP Tool Returns Null
Verify Azure DevOps organization and project names are correct in `.env`.

### No Logs Appearing
Enable debug logging:
```
LOG_LEVEL=DEBUG
```

Logs are written to `logs/agent.log`. Check that file for detailed output.

## Architecture

The agent follows a modular architecture:

- **Agent** (`src/agent.py`): Core orchestration with dynamic instructions
- **MCP Handler**: Automatic Azure DevOps connection via MCP
- **REST API** (`src/api.py`): Multi-platform access with streaming
- **Instruction Sets** (`config/instructions_*.md`): Pluggable behavioral modes

The system automatically:
1. Connects to Azure DevOps via MCP
2. Loads instruction set for the active mode
3. Processes queries with GPT-4o
4. Returns structured output (JSON + human-readable)
5. Clears logs on each restart for clean sessions

## Development

### Local Testing

```bash
# Test routing
.\routing.ps1 676893

# Test summary
.\query.ps1 "Show action 676893"

# Test custom query
.\query.ps1 "List all active actions"
```

### Debug Mode

Enable detailed logging:
```bash
LOG_LEVEL=DEBUG python run_api.py
```

### Code Standards

Before committing:
```bash
pytest tests/              # Run tests
black src/                 # Format code
pylint src/                # Lint code
```

## Contributing

1. Create feature branch from `main`
2. Make changes with descriptive commits
3. Update tests and documentation
4. Submit PR with summary of changes

## Roadmap

- ✅ **Phase 1**: Simple Model Interaction
- ✅ **Phase 2**: MCP Integration with Azure DevOps
- ✅ **Phase 2b**: Dynamic Instructions & Routing Analysis
- 🔲 **Phase 3**: Multi-Platform Deployment (Teams, Web, PowerBI)

## Support

For issues or questions:
- Check [QUICKSTART.md](QUICKSTART.md) for setup help
- Review [Routing Instructions](config/instructions_routing.md) for analysis details
- See [DYNAMIC_INSTRUCTIONS.md](DYNAMIC_INSTRUCTIONS.md) for advanced patterns
- Enable `LOG_LEVEL=DEBUG` for troubleshooting

## License

See [LICENSE](LICENSE) for details.
