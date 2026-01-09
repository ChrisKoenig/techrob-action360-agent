# TechRob Action360 Agent - Project Guidelines

## Project Overview
A flexible, multi-platform AI agent built with Microsoft Agent Framework that connects to Azure DevOps MCP server and uses Azure AI Foundry's GPT-4o model.

## Git & Repository
- **Repository**: https://github.com/ChrisKoenig/techrob-action360-agent
- **Branching Strategy**: Main branch for production, feature branches for development
- **Commit Convention**: Descriptive messages following conventional commits
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `refactor:` for code improvements
  - `test:` for test additions

## Architecture
- **Agent Framework**: Microsoft Agent Framework (Python)
- **Model**: Azure AI Foundry GPT-4o
- **Server Integration**: Model Context Protocol (MCP) with Azure DevOps ✅
- **API**: REST API for multi-platform access
- **Tools**: Work items, pull requests, pipelines, team capacity

## Key Components
- `src/agent.py` - Core agent with MCP tool integration
- `src/mcp_handler.py` - Azure DevOps MCP server connection handler
- `src/api.py` - REST API server for multi-platform access
- `config/agent_config.yaml` - Agent and MCP configuration
- `example_mcp_integration.py` - Azure DevOps integration examples
- `tests/` - Unit and integration tests

## Development Workflow

### Local Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install deps: `pip install -r requirements.txt --pre`
5. Copy `.env.example` to `.env` and configure
6. Login to Azure: `az login`

### Running the Agent
- Examples: `python example_mcp_integration.py`
- API: `python run_api.py`
- Tests: `pytest tests/`

### Before Committing
- Run tests: `pytest tests/`
- Format code: `black src/`
- Lint: `pylint src/`
- Update docs if needed

## Phases & Roadmap

### Phase 1: Simple Model Interaction ✅
- Core agent with Foundry GPT-4o
- REST API with streaming
- Basic examples

### Phase 2: MCP Integration ✅
- Azure DevOps MCP server connection
- Work items, pull requests, pipeline tools
- Team capacity and iteration management
- Comprehensive examples and documentation

### Phase 3: Multi-Platform Deployment (Next)
- Teams/M365 Copilot plugin
- Web app integration
- PowerBI custom functions
- Thread persistence

## Azure DevOps Organization
- **Name**: UnifiedActionTracker
- **MCP Command**: `npx -y @azure-devops/mcp@next UnifiedActionTracker`
- **Auth**: Azure CLI (`az login`)

## Next Steps
1. Run `python example_mcp_integration.py` to explore MCP integration
2. Test queries against UnifiedActionTracker
3. Implement Phase 3: Multi-platform deployment
