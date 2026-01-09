# Phase 2: Azure DevOps MCP Integration

## Overview

Phase 2 adds full Azure DevOps integration via the Model Context Protocol (MCP). The agent can now connect to your UnifiedActionTracker Azure DevOps organization and access tools for work item management, pull requests, pipelines, and more.

## What's New

### Core Components

1. **Enhanced Agent** (`src/agent.py`)
   - Now loads Azure DevOps MCP tools
   - Uses `MCPStdioTool` from Agent Framework
   - Custom instructions for Azure DevOps workflows
   - Tool information endpoint

2. **MCP Handler** (`src/mcp_handler.py`)
   - Manages MCP server lifecycle (start/stop)
   - Builds command to launch Azure DevOps MCP
   - Provides async context manager for connection management

3. **Updated Config** (`config/agent_config.yaml`)
   - MCP configuration with ADO organization
   - Command and args for launching MCP server
   - Enhanced system prompt for ADO workflows

4. **MCP Integration Example** (`example_mcp_integration.py`)
   - 6 complete example scenarios
   - Work items, pull requests, pipelines
   - Team capacity and specialized agents
   - Copy-paste ready queries

## Configuration

### Environment Variables

Edit `.env` with:

```bash
# Required
FOUNDRY_PROJECT_ENDPOINT=https://<region>.api.azureml.ms
MODEL_DEPLOYMENT=gpt-4o

# Azure DevOps
ADO_ORG_NAME=UnifiedActionTracker
```

### MCP Server Setup

The agent automatically launches the Azure DevOps MCP server using:

```bash
npx -y @azure-devops/mcp@next UnifiedActionTracker
```

**Requirements:**
- Node.js and npm installed
- Azure DevOps credentials (via `az login` or other auth methods)
- Access to UnifiedActionTracker organization

## Available Azure DevOps Tools

The MCP server provides tools across multiple domains:

### Work Items
- `wit_my_work_items` - Get your assigned work items
- `wit_create_work_item` - Create tasks, bugs, features
- `wit_update_work_item` - Modify work item details
- `wit_list_backlogs` - View backlog structure
- `wit_get_work_items_batch_by_ids` - Bulk retrieve items
- `wit_add_work_item_comment` - Add comments

### Pull Requests
- `repo_list_pull_requests_by_repo_or_project` - Find PRs
- `repo_create_pull_request` - Create new PR
- `repo_update_pull_request` - Modify PR details
- `repo_list_pull_request_threads` - Get code review threads
- `repo_create_pull_request_thread` - Start review discussion

### Pipelines
- `pipelines_list_runs` - View recent pipeline runs
- `pipelines_get_run` - Get specific run details
- `pipelines_get_build_status` - Check build status
- `pipelines_run_pipeline` - Trigger pipeline execution
- `pipelines_update_build_stage` - Manage build stages

### Repositories
- `repo_list_repos_by_project` - List all repos
- `repo_create_branch` - Create feature branches
- `repo_list_branches_by_repo` - View branches
- `repo_search_commits` - Find commits by criteria

### Team & Capacity
- `work_list_iterations` - View sprints/iterations
- `work_list_team_iterations` - Team sprint assignments
- `work_get_team_capacity` - Team capacity metrics
- `work_update_team_capacity` - Set capacity for members

### Projects & Teams
- `core_list_projects` - List all projects
- `core_list_project_teams` - List project teams
- `core_get_identity_ids` - Search team members

## Usage Examples

### Simple Query

```python
import asyncio
from src.agent import TechRobAgent

async def main():
    agent = TechRobAgent()
    
    response = await agent.process_query(
        "List my high-priority work items in the UnifiedActionTracker project"
    )
    print(response)
    
    await agent.cleanup()

asyncio.run(main())
```

### Streaming Response

```python
async for chunk in agent.process_query_stream(
    "Create a summary of completed items this sprint"
):
    print(chunk, end="", flush=True)
```

### Custom System Prompt

```python
agent = TechRobAgent(
    instructions="You are a project manager assistant. Focus on sprint health and team capacity."
)
```

## Example Queries

### Work Items
- "Create a bug in the UnifiedActionTracker project: Server returning 500 errors"
- "Show me all unresolved bugs assigned to me"
- "Update work item 1234: Change status to 'In Progress'"
- "Link work item 999 as parent of work item 1000"

### Pull Requests
- "Create a pull request from 'feature/auth' to 'main' with title 'Add OAuth integration'"
- "List all open pull requests waiting for review"
- "Get the conversation on pull request 42"

### Pipelines
- "What's the status of the latest build?"
- "Show me any failed pipeline runs from today"
- "Trigger the 'deploy-production' pipeline"

### Team Capacity
- "What's our team capacity for the current sprint?"
- "Show me the backlog for this iteration"
- "Who has capacity to take on new work?"

## Running the Examples

```bash
# View available examples
python example_mcp_integration.py

# Or run programmatically:
# 1. Edit example_mcp_integration.py
# 2. Uncomment desired examples in main()
# 3. Run: python example_mcp_integration.py
```

## Architecture Flow

```
User Query
    ↓
Agent Framework (GPT-4o)
    ↓
MCP Stdio Tool
    ↓
Azure DevOps MCP Server (npx @azure-devops/mcp@next)
    ↓
Azure DevOps REST API
    ↓
Response (formatted by agent)
    ↓
Back to User
```

## Troubleshooting

### MCP Server Won't Start

1. Check Node.js is installed: `node --version`
2. Verify npm cache: `npm cache clean --force`
3. Check credentials: `az login`
4. Try manual launch: `npx -y @azure-devops/mcp@next UnifiedActionTracker`

### Tool Not Found Error

- Ensure `@azure-devops/mcp@next` is available via npm
- May require internet connection for first download
- Check VS Code MCP Explorer for tool list

### Azure Authentication Failed

- Run: `az login`
- Set `ADO_ORG_NAME` correctly
- Verify your organization name in Azure DevOps URL

### Agent Ignores MCP Tools

- Ensure `enable_mcp=True` (default)
- Check logs for initialization errors
- Verify Foundry credentials are valid

## Next Phase

Phase 3 will add:
- Multi-platform deployment (Teams, web app, PowerBI)
- Thread persistence for conversation history
- Custom tool creation
- Workflow orchestration

## References

- [Azure DevOps MCP GitHub](https://github.com/microsoft/azure-devops-mcp)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Agent Framework Docs](https://github.com/microsoft/agent-framework)
