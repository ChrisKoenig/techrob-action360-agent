# TechRob Action360 Agent - Project Guidelines

## Project Overview
A flexible, multi-platform AI agent built with Microsoft Agent Framework that connects to MCP servers and uses Azure AI Foundry's GPT-4o model.

## Architecture
- **Agent Framework**: Microsoft Agent Framework (Python)
- **Model**: Azure AI Foundry GPT-4o
- **Server Integration**: Model Context Protocol (MCP)
- **API**: REST API for multi-platform access

## Key Components
- `src/agent.py` - Core agent implementation
- `src/mcp_handler.py` - MCP server connection handler
- `src/api.py` - REST API server
- `config/` - Configuration files

## Next Steps
1. Configure Azure Foundry credentials in `.env`
2. Set up MCP server connection details
3. Implement MCP tool integration
4. Configure agent behavior and system prompt
5. Deploy REST API and integrate with Teams/web apps
