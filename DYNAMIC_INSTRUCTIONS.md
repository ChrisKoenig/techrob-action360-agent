# Dynamic Instructions Guide

## Overview

The TechRob Action360 Agent now supports **dynamic instruction sets**, allowing you to switch between different behavioral modes without creating separate agents. This is useful for different query types that require different analysis approaches.

## Available Instruction Sets

### `summary` (Default)
**File**: `config/instructions_summary.md`

Used for retrieving and summarizing Actions. Focuses on:
- Action details and metadata
- Related tickets and actions
- Clear, structured formatting
- Single item lookups and list queries

**Use when**: You need to retrieve information about Actions, get summaries, or generate lists.

### `routing` 
**File**: `config/instructions_routing.md`

Used for analyzing Actions through a deterministic 7-phase routing engine. Focuses on:
- **Phase 1**: Data extraction and normalization from work item
- **Phase 2**: Requestor identity classification (CSU vs STU)
- **Phase 3**: Service-to-solution-area mapping
- **Phase 4**: Mutually exclusive rules (capacity, security, modern work, scheduled items)
- **Phase 5**: Direct routing rules (Enterprise Modernization, Service Availability, Platform Development, etc.)
- **Phase 5B**: Mandatory milestone verification
- **Phase 6**: Non-mutually exclusive secondary rules
- **Phase 7**: Output formatting (human-readable + JSON)

**Routing Output**:
- Assigned team (e.g., "Tech RoB", "Platform Team")
- Assigned milestone/solution area (e.g., "Service Availability", "Enterprise Modernization")
- Service identification
- Requestor and context information
- Structured JSON with decision reasoning

**Use when**: You need to analyze an Action and determine the optimal team/area for assignment using deterministic rules.

## Usage Examples

### Summary Mode: Quick Lookup

```bash
.\query.ps1 "Show action 676893"
```

Returns:
```
Action ID: 676893
Title: PostgreSQL Database Connection Issue
Status: Active
Service: Database Infrastructure
Requestor: Unity Technologies Engineering
Created: 2024-01-15
Priority: High
```

### Routing Mode: Analysis with Assignment

```bash
.\routing.ps1 676893
```

Returns:
```
Routing Decision: Tech RoB | Service Availability
Requestor: Unity Technologies (engineering-team@unity.com)
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

{Complete JSON output with all phase results}
```

### Python: Dynamic Switching

```python
import asyncio
from src.agent import TechRobAgent

async def analyze_and_route():
    agent = TechRobAgent(instruction_type="summary")
    await agent.initialize()
    
    # Get summary
    print("=== SUMMARY ===")
    summary = await agent.process_query("Show action 676893")
    print(summary)
    
    # Switch to routing
    print("\n=== ROUTING ANALYSIS ===")
    agent.set_instruction_type("routing")
    routing = await agent.process_query("Analyze action 676893 for routing")
    print(routing)
    
    await agent.cleanup()

asyncio.run(analyze_and_route())
```

### REST API: Routing with Streaming

```bash
curl -X POST http://localhost:8000/api/query/stream \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze action 676893 and provide routing recommendation",
    "instruction_type": "routing"
  }'
```

This returns chunked Server-Sent Events for real-time display of routing analysis.

## REST API Support

The REST API fully supports instruction types:

```powershell
# Summary mode (default if not specified)
curl -X POST http://localhost:8000/api/query `
  -H "Content-Type: application/json" `
  -d '{"query": "Show me action 12345"}'

# Routing mode
curl -X POST http://localhost:8000/api/query `
  -H "Content-Type: application/json" `
  -d '{
    "query": "Analyze action 12345 for routing",
    "instruction_type": "routing"
  }'

# Streaming (real-time output)
curl -X POST http://localhost:8000/api/query/stream `
  -H "Content-Type: application/json" `
  -d '{
    "query": "Analyze action 12345 for routing",
    "instruction_type": "routing"
  }'
```

## Usage Patterns

### Pattern 1: Create Agent with Specific Instruction Type

```python
from src.agent import TechRobAgent

# Create agent in routing mode
agent = TechRobAgent(instruction_type="routing")
await agent.initialize()

response = await agent.process_query("Analyze action 676893 for routing")
```

### Pattern 2: Default Mode (Summary)

```python
# If you don't specify instruction_type, it defaults to "summary"
agent = TechRobAgent()
await agent.initialize()

response = await agent.process_query("Show me action 12345")
```

### Pattern 3: Dynamic Switching

```python
agent = TechRobAgent(instruction_type="summary")
await agent.initialize()

# Get summary
summary = await agent.process_query("Show action 676893")

# Switch to routing mode
agent.set_instruction_type("routing")

# Get routing recommendation for the same action
routing = await agent.process_query("Analyze this action for routing")

# Switch back
agent.set_instruction_type("summary")
```

## Query Patterns by Instruction Type

### Summary Mode Queries
- "Show action 12345"
- "What is action 676893?"
- "List the details of work item 54321"
- "Get information about action 111222"
- "Summarize action 999888"

### Routing Mode Queries
- "Analyze action 676893 for routing"
- "Where should action 54321 be routed?"
- "Determine the routing decision for action 12345"
- "Provide routing recommendation for work item 111"
- "Route action 676893"

## Extending with Custom Instructions

To add a new instruction type:

1. Create a new file: `config/instructions_<typename>.md`
2. Define your instructions following the same format as existing files
3. Use it:
   ```python
   agent = TechRobAgent(instruction_type="<typename>")
   ```

The agent automatically discovers and loads any `instructions_*.md` file.

## Implementation Details

### Agent Constructor Parameters

```python
TechRobAgent(
    project_endpoint: Optional[str] = None,
    model_deployment_name: Optional[str] = None,
    ado_org_name: Optional[str] = None,
    ado_project_name: Optional[str] = None,
    agent_name: str = "TechRobAction360Agent",
    instructions: Optional[str] = None,      # Override with custom string
    instruction_type: str = "summary",       # NEW: Type of instructions to load
    enable_mcp: bool = True,
)
```

### New Methods

#### `set_instruction_type(instruction_type: str)`

Dynamically change the instruction set:

```python
agent.set_instruction_type("routing")
```

This method:
- Updates `agent.instruction_type`
- Reloads instructions from the corresponding file
- Takes effect on the next `process_query()` call

## Example Scripts

### Summary Mode Example

```bash
python example_simple.py
```

### Dynamic Instructions Example

```bash
python example_dynamic_instructions.py
```

This script demonstrates:
1. Summary mode query
2. Routing mode query
3. Dynamic switching within same agent
4. Streaming with different instructions

## Backward Compatibility

- **Default behavior unchanged**: If you don't specify `instruction_type`, it defaults to `"summary"`
- **Legacy files supported**: If `instructions_<type>.md` doesn't exist, the agent falls back to `instructions.md` (if present)
- **Custom instructions still work**: You can override with a custom instruction string via the `instructions` parameter

## Best Practices

1. **Use explicit instruction_type**: Make your code clear about which mode you're in
   ```python
   agent = TechRobAgent(instruction_type="routing")  # Clear intent
   ```

2. **Don't mix concerns**: For complex workflows, consider separate agents for different tasks
   ```python
   summary_agent = TechRobAgent(instruction_type="summary")
   routing_agent = TechRobAgent(instruction_type="routing")
   ```

3. **Document custom instructions**: If you add new instruction types, document their purpose and usage

4. **Test instruction changes**: When switching instructions, verify the agent's behavior matches expectations
   ```python
   agent.set_instruction_type("new_type")
   response = await agent.process_query("Test query")
   # Verify response format matches new instructions
   ```

## Troubleshooting

### Instructions not loading
- Check that the file exists: `config/instructions_<type>.md`
- Check file permissions
- Review logs for error messages
- Fallback to default instructions will be used automatically

### Agent behavior doesn't match instructions
- Verify `agent.instruction_type` is what you expect
- Check that the instruction file was modified correctly
- Review the query to ensure it aligns with the instruction intent

### REST API doesn't support instruction_type
- Update `src/api.py` to accept and pass `instruction_type` parameter
- See REST API Support section above
