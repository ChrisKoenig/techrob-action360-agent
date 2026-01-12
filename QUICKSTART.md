# Quick Start - TechRob Action360 Agent

**5-minute setup to running routing analysis.**

## 1. Prerequisites

✅ Azure CLI installed and logged in:
```bash
az login
```

✅ Python 3.10+ installed

✅ Node.js 16+ installed (for MCP)

## 2. Clone and Setup

```bash
git clone https://github.com/ChrisKoenig/techrob-action360-agent.git
cd techrob-action360-agent

python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
cp .env.example .env
```

## 3. Configure .env

Edit `.env` with your Azure details:

```bash
FOUNDRY_PROJECT_ENDPOINT=https://<region>.api.azureml.ms
FOUNDRY_PROJECT_NAME=<your-project>
FOUNDRY_RESOURCE_GROUP=<your-rg>
FOUNDRY_SUBSCRIPTION_ID=<your-sub>
ADO_ORG_NAME=<your-ado-org>
ADO_PROJECT_NAME=<your-ado-project>
```

## 4. Start the API Server

```bash
python run_api.py
```

Server running at `http://localhost:8000`. Logs to `logs/agent.log`.

## 5. Test Routing Analysis

### Using PowerShell

```powershell
.\routing.ps1 676893
```

Returns:
- Routing decision (e.g., "Tech RoB | Service Availability")
- Requestor information
- Service and context
- Identified asks
- Machine-readable JSON

### Using curl

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze action 676893 and provide routing recommendation",
    "instruction_type": "routing"
  }'
```

### Using Python

```python
import asyncio
from src.agent import TechRobAgent

async def analyze():
    agent = TechRobAgent(instruction_type="routing")
    await agent.initialize()
    result = await agent.process_query("Analyze action 676893")
    print(result)
    await agent.cleanup()

asyncio.run(analyze())
```

## 6. Try Summary Mode

For quick lookups without routing analysis:

```bash
.\query.ps1 "Show action 676893"
```

## What's Happening

1. **Agent** connects to Azure AI Foundry GPT-4o
2. **MCP** automatically connects to your Azure DevOps organization
3. **Query** is processed with the selected instruction set
4. **Work item** is fetched via MCP tools from Azure DevOps
5. **Analysis** applies routing rules (or summary rules)
6. **Response** returns routing decision with reasoning

## Next Steps

- Read [Routing Instructions](config/instructions_routing.md) to understand the 7-phase routing engine
- See [Dynamic Instructions Guide](DYNAMIC_INSTRUCTIONS.md) for advanced patterns
- Check [README.md](README.md) for full API documentation
- Review logs in `logs/agent.log` for debugging

## Troubleshooting

**"No credentials found"**: Run `az login` first

**"Work item not found"**: Verify action ID exists in your Azure DevOps project

**"Port 8000 already in use"**: Change `API_PORT` in `.env` (try `8001`)

**No output in PowerShell**: Copy the full `.ps1` file path or use Python directly

## Instruction Types

The agent supports two main modes:

### Summary Mode
Quick lookups and information retrieval.
```bash
.\query.ps1 "Show me action 12345"
.\query.ps1 "List all active actions"
```

### Routing Mode  
Comprehensive 7-phase routing analysis that determines optimal team/area for each Action.
```bash
.\routing.ps1 676893
.\routing.ps1 "Analyze action 123456"
```

For details, see [DYNAMIC_INSTRUCTIONS.md](DYNAMIC_INSTRUCTIONS.md).

## API Reference

### GET /api/health
Check if the server is running.
```bash
curl http://localhost:8000/api/health
```

### POST /api/query
Send a query with a specific instruction type.
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Your query here",
    "instruction_type": "routing"
  }'
```

### POST /api/query/stream
Stream response as Server-Sent Events (useful for long responses).
```bash
curl -X POST http://localhost:8000/api/query/stream \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze action 676893",
    "instruction_type": "routing"
  }'
```

### GET /api/tools
List available tools and instruction types.
```bash
curl http://localhost:8000/api/tools
```

## Need Help?

- **Setup issues?** Check Azure CLI login: `az login`
- **Port conflicts?** Change `API_PORT` in `.env`
- **Missing work items?** Verify project name in `.env` matches Azure DevOps
- **Debug mode?** Set `LOG_LEVEL=DEBUG` and check `logs/agent.log`

See [README.md](README.md) for complete documentation.
