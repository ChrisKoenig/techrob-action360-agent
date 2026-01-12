# Phase 2: Azure DevOps MCP Integration - COMPLETED ✅

## Status

**Production Ready** - Full MCP integration with dynamic routing analysis.

The agent now has production-grade Azure DevOps MCP integration with deterministic routing analysis. All components are working and validated with real data.

## What's Included

### 1. Automatic MCP Tool Integration

The agent automatically connects to Azure DevOps and provides access to:

- **Work Items**: Fetch, create, and update actions
- **Pull Requests**: Access PR data and status
- **Pipelines**: Retrieve build and pipeline information
- **Team Capacity**: Get team availability and capacity data
- **Iterations**: Access iteration and sprint information

**How it works** (`src/agent.py`):
```python
# Agent automatically launches MCP server with project context
mcp_args = [
    "-y",
    "@azure-devops/mcp@next",
    self.ado_org_name,        # e.g., "UnifiedActionTracker"
    self.ado_project_name,    # e.g., "Unified Action Tracker"
]
```

### 2. Dynamic Instruction Architecture

The agent loads different instruction sets based on the mode:

**Summary Mode** (default) - Quick lookups and information retrieval:
```python
agent = TechRobAgent(instruction_type="summary")
await agent.initialize()
response = await agent.process_query("Show action 676893")
```

**Routing Mode** - Comprehensive 7-phase routing analysis:
```python
agent = TechRobAgent(instruction_type="routing")
await agent.initialize()
response = await agent.process_query("Analyze action 676893")
```

Instruction files:
- `config/instructions_summary.md` - Summary mode instructions
- `config/instructions_routing.md` - Routing mode instructions (7 phases)

### 3. The 7-Phase Routing Engine

When in routing mode, the agent analyzes Actions through 7 phases:

**Phase 1: Data Extraction & Normalization**
- Extract relevant fields from work item
- Parse requestor information
- Identify service and context

**Phase 2: Requestor Identity Classification**
- Determine if requestor is CSU (Corporate Services Unit) or STU (Service Team Unit)
- Extract organization and contact information

**Phase 3: Service-to-Solution-Area Mapping**
- Map identified service to solution areas
- Identify primary service category

**Phase 4: Mutually Exclusive Rules** (Applied if conditions met)
- Capacity constraints check
- Security and compliance requirements
- Modern work requirements
- Scheduled/planned items

**Phase 5: Direct Routing Rules** (Milestone-driven)
- Enterprise Modernization routing
- Service Availability routing
- Platform Development routing
- Infrastructure & Cloud Services routing
- Organizational Effectiveness routing

**Phase 5B: Mandatory Milestone Check**
- Ensure milestone is present in final decision

**Phase 6: Non-Mutually Exclusive Rules**
- Apply secondary routing factors
- Handle special cases

**Phase 7: Output Formatting**
- Generate human-readable summary
- Create machine-readable JSON output

### 4. REST API with Streaming

Multi-platform access with Server-Sent Events:

```bash
# Non-streaming query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze action 676893", "instruction_type": "routing"}'

# Streaming query (real-time output)
curl -X POST http://localhost:8000/api/query/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze action 676893", "instruction_type": "routing"}'
```

Endpoints:
- `GET /api/health` - Health check
- `POST /api/query` - Standard query response
- `POST /api/query/stream` - Streaming response (Server-Sent Events)
- `GET /api/tools` - List available tools and instruction types

### 5. PowerShell Command-Line Interface

Quick access scripts:

```powershell
# Routing analysis
.\routing.ps1 676893

# Summary lookup
.\query.ps1 "Show action 676893"

# Custom query
.\query.ps1 "Analyze action 123456"
```

## Configuration

Edit `.env` with your Azure details:

```bash
# Azure AI Foundry
FOUNDRY_PROJECT_ENDPOINT=https://<region>.api.azureml.ms
FOUNDRY_PROJECT_NAME=<your-project-name>
FOUNDRY_RESOURCE_GROUP=<your-resource-group>
FOUNDRY_SUBSCRIPTION_ID=<your-subscription-id>
MODEL_DEPLOYMENT=gpt-4o

# Azure DevOps
ADO_ORG_NAME=UnifiedActionTracker
ADO_PROJECT_NAME=Unified Action Tracker

# API Settings
API_PORT=8000
API_HOST=0.0.0.0
LOG_LEVEL=INFO
```

## How It Works

### 1. Agent Initialization

When the agent starts, it:
1. Loads Azure credentials via Azure CLI
2. Connects to Azure AI Foundry GPT-4o deployment
3. Launches Azure DevOps MCP server with organization and project context
4. Registers MCP tools for work item access
5. Loads instruction set for active mode

### 2. Query Processing

When you query the agent:
1. Query arrives at REST API (`POST /api/query` or `/api/query/stream`)
2. Agent applies current instruction set
3. Agent uses MCP tools to fetch work item from Azure DevOps
4. GPT-4o analyzes work item against routing rules (or summary rules)
5. Response is returned (streaming or complete)

### 3. Instruction Type Switching

You can switch instruction types without restarting:

```python
agent = TechRobAgent(instruction_type="summary")
await agent.initialize()

# Later, switch to routing
agent.set_instruction_type("routing")
result = await agent.process_query("Analyze action 676893")
```

## Testing

### Quick Test

```powershell
# Start server
python run_api.py

# In another terminal, test routing
.\routing.ps1 676893
```

### Expected Output

For a valid action, routing mode returns:

```
Routing Decision: Tech RoB | Service Availability
Requestor: [Organization/Contact Info]
Service: [Service Name]
Context: [Context Information]
Identified Asks: [Main requests or issues]

{JSON formatted output with all analysis details}
```

## Logging

Logs are written to `logs/agent.log` and auto-cleared on each server restart.

Enable debug logging to see detailed operation flow:
```bash
LOG_LEVEL=DEBUG python run_api.py
```

Log entries include:
- MCP tool initialization
- Work item fetch operations
- Instruction loading
- Routing phase execution
- Final decision output

## Troubleshooting

### MCP Tool Returns Null

**Symptom**: Work items not found by MCP tools

**Solution**: Verify Azure DevOps details in `.env`:
```bash
ADO_ORG_NAME=UnifiedActionTracker
ADO_PROJECT_NAME=Unified Action Tracker
```

### Authentication Error

**Symptom**: "No credentials found" or Azure connection fails

**Solution**: Login to Azure CLI:
```bash
az login
```

### Port Already in Use

**Symptom**: "Address already in use" when starting server

**Solution**: Change port in `.env`:
```bash
API_PORT=8001
```

### No Routing Decision Returned

**Symptom**: Agent returns "Missing Data" or partial response

**Reasons**:
- Work item doesn't exist in Azure DevOps
- Required fields are missing from work item
- MCP tool couldn't fetch complete data

**Solution**: Check logs with `LOG_LEVEL=DEBUG` and verify action exists in Azure DevOps.

## File Structure

```
src/agent.py          # Core agent with MCP and instruction switching
src/api.py            # REST API with streaming support
config/instructions_summary.md   # Summary mode instructions
config/instructions_routing.md   # Routing mode instructions (7 phases)
run_api.py            # API server launcher
routing.ps1           # PowerShell routing script
query.ps1             # PowerShell summary script
logs/agent.log        # Agent execution logs (auto-cleared on startup)
```

## Example Outputs

### Routing Analysis Example

Input: `Analyze action 676893`

Output:
```
[Analysis complete]

ROUTING DECISION: Tech RoB | Service Availability

Requestor Organization: Unity Technologies
Contact: engineering-team@unity.com

Service: PostgreSQL/Database
Context: Production incident - critical database connectivity issue

Identified Asks:
1. Restore database connectivity
2. Prevent future outages
3. Implement monitoring

Routing Rationale:
- Service maps to Platform/Service Availability
- Severity indicates immediate Team RoB assignment
- Database expertise required in service area

JSON Output:
{
  "routing_team": "Tech RoB",
  "milestone": "Service Availability",
  "service": "PostgreSQL",
  "urgency": "critical",
  "phases_applied": [1, 2, 3, 5, 7]
}
```

## Next Steps

1. **Use the agent**: Start with QUICKSTART.md for immediate usage
2. **Customize routing**: Edit `config/instructions_routing.md` for your needs
3. **Integrate with tools**: Add custom MCP servers or tools as needed
4. **Deploy**: Phase 3 will add Teams/M365 integration

See [README.md](README.md) for full documentation.
