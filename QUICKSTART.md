# Quick Start Guide - TechRob Action360 Agent

## Setup

### 1. Configure Your Environment

Edit `.env` with your Azure/Foundry credentials:

```bash
cp .env.example .env
```

Required settings in `.env`:
- `FOUNDRY_PROJECT_ENDPOINT` - Your Foundry project endpoint (e.g., `https://eastus.api.azureml.ms`)
- `MODEL_DEPLOYMENT` - Your deployed model name (e.g., `gpt-4o`)

You need valid Azure credentials on your machine (via Azure CLI, managed identity, or environment variables).

### 2. Install Dependencies

```bash
pip install -r requirements.txt --pre
```

The `--pre` flag is required because Agent Framework is in preview.

---

## Running the Agent

### Simple Query Example

Test basic agent functionality:

```bash
python example_simple.py
```

This runs three examples:
1. **Simple Query** - Basic Q&A
2. **Streaming Query** - Real-time text streaming
3. **Custom Instructions** - Agent with specialized behavior

### Start the REST API Server

Launch the API for multi-platform access:

```bash
python run_api.py
```

The API will be available at `http://localhost:8000`

---

## API Endpoints

### Non-Streaming Query
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
```

Response:
```json
{
  "query": "What is machine learning?",
  "response": "Machine learning is..."
}
```

### Streaming Query (Server-Sent Events)
```bash
curl -X POST http://localhost:8000/api/query/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum computing"}' \
  -N
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

### List Tools
```bash
curl http://localhost:8000/api/tools
```

---

## Using in Python Code

### Simple Usage

```python
import asyncio
from src.agent import TechRobAgent

async def main():
    agent = TechRobAgent()
    
    # Single query
    response = await agent.process_query("Hello!")
    print(response)
    
    await agent.cleanup()

asyncio.run(main())
```

### Streaming Usage

```python
async def main():
    agent = TechRobAgent()
    
    # Stream response
    async for chunk in agent.process_query_stream("Write a poem"):
        print(chunk, end="", flush=True)
    
    await agent.cleanup()

asyncio.run(main())
```

### Custom System Prompt

```python
agent = TechRobAgent(
    instructions="You are a helpful coding assistant. Always explain your answers."
)
```

---

## Next Steps

Once you have this working:

1. **Add MCP Tools** - Connect to external services via MCP server
2. **Configure Thread Persistence** - Store conversation history
3. **Deploy to Teams** - Register agent as M365 Copilot plugin
4. **Integrate with Web App** - Call the REST API from your frontend
5. **Connect PowerBI** - Use the API endpoint in custom PowerBI functions

---

## Troubleshooting

### Authentication Error
Make sure you have Azure credentials configured:
```bash
az login
```

### Port Already in Use
Change the port in `.env`:
```
API_PORT=8001
```

### Model Not Found
Verify the model is deployed in your Foundry project:
- Go to your Foundry project
- Check **Deployments** section
- Confirm deployment name matches `MODEL_DEPLOYMENT` in `.env`

### No Response from Agent
Check logs for error messages. Enable debug logging:
```
LOG_LEVEL=DEBUG
```

---

## Architecture

```
TechRob Action360 Agent
│
├── src/agent.py              # Core agent with Foundry integration
├── src/api.py                # REST API (POST /api/query, /api/query/stream)
├── src/mcp_handler.py        # MCP integration (future)
└── config/                   # Configuration files
```

The agent is intentionally simple now - just Foundry + GPT-4o. MCP tools will be added in the next phase without changing the core structure.
