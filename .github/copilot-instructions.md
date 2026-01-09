# TechRob Action360 Agent - Project Guidelines

## Project Overview
A flexible, multi-platform AI agent built with Microsoft Agent Framework that connects to MCP servers and uses Azure AI Foundry's GPT-4o model.

## Git & Repository
- **Repository**: Git-based version control
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
- **Server Integration**: Model Context Protocol (MCP) - phase 2
- **API**: REST API for multi-platform access

## Key Components
- `src/agent.py` - Core agent implementation with Foundry integration
- `src/api.py` - REST API server for multi-platform access
- `src/mcp_handler.py` - MCP server connection handler (future)
- `config/` - Configuration files
- `tests/` - Unit and integration tests
- `example_simple.py` - Example usage and testing

## Development Workflow

### Local Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install deps: `pip install -r requirements.txt --pre`
5. Copy `.env.example` to `.env` and configure

### Running the Agent
- Examples: `python example_simple.py`
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

### Phase 2: MCP Integration (Next)
- Connect to MCP servers
- Add tool definitions
- Integrate tools into agent

### Phase 3: Multi-Platform Deployment
- Teams/M365 Copilot plugin
- Web app integration
- PowerBI custom functions

## Next Steps
1. Configure Azure Foundry credentials in `.env`
2. Test with `python example_simple.py`
3. Start API with `python run_api.py`
4. Begin Phase 2: MCP integration
