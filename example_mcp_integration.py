#!/usr/bin/env python3
"""
Azure DevOps MCP Integration Examples for TechRob Action360 Agent.

This demonstrates how the agent uses Azure DevOps MCP tools to:
- Query work items
- Manage pull requests
- Monitor pipelines
- Manage team capacity
"""

import asyncio
import logging
import os
from dotenv import load_dotenv
from src.agent import TechRobAgent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def example_work_items():
    """Example: Query and manage work items."""
    logger.info("=" * 70)
    logger.info("EXAMPLE 1: Work Items Management")
    logger.info("=" * 70)
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        ado_org_name=os.getenv("ADO_ORG_NAME"),
    )
    
    try:
        # Query: Get all high-priority bugs assigned to me
        response = await agent.process_query(
            "Show me all high-priority bugs assigned to me in the UnifiedActionTracker project"
        )
        print(f"\nAgent Response:\n{response}\n")
        
        # Query: Create a new task
        response = await agent.process_query(
            "Create a new task in UnifiedActionTracker project with title 'Implement Azure DevOps MCP integration' "
            "and description 'Add MCP tools to TechRob agent'"
        )
        print(f"\nAgent Response:\n{response}\n")
    finally:
        await agent.cleanup()


async def example_pull_requests():
    """Example: Manage pull requests."""
    logger.info("=" * 70)
    logger.info("EXAMPLE 2: Pull Requests Management")
    logger.info("=" * 70)
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        ado_org_name=os.getenv("ADO_ORG_NAME"),
    )
    
    try:
        # Query: Get open pull requests
        response = await agent.process_query(
            "List all open pull requests in the main branch of my repositories"
        )
        print(f"\nAgent Response:\n{response}\n")
        
        # Query: Create a PR
        response = await agent.process_query(
            "I have a feature branch 'feature/mcp-integration' ready for review. "
            "Create a pull request to merge it into main with title 'Add MCP integration' "
            "and a detailed description of the changes"
        )
        print(f"\nAgent Response:\n{response}\n")
    finally:
        await agent.cleanup()


async def example_pipelines():
    """Example: Monitor and manage pipelines."""
    logger.info("=" * 70)
    logger.info("EXAMPLE 3: Pipeline Management")
    logger.info("=" * 70)
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        ado_org_name=os.getenv("ADO_ORG_NAME"),
    )
    
    try:
        # Query: Get recent builds
        response = await agent.process_query(
            "What are the recent pipeline runs? Show me any failed builds and their error details."
        )
        print(f"\nAgent Response:\n{response}\n")
    finally:
        await agent.cleanup()


async def example_team_capacity():
    """Example: Manage team capacity and iterations."""
    logger.info("=" * 70)
    logger.info("EXAMPLE 4: Team Capacity & Iterations")
    logger.info("=" * 70)
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        ado_org_name=os.getenv("ADO_ORG_NAME"),
    )
    
    try:
        # Query: Get current iteration
        response = await agent.process_query(
            "What's the current sprint/iteration? Show me the team capacity and any available bandwidth."
        )
        print(f"\nAgent Response:\n{response}\n")
    finally:
        await agent.cleanup()


async def example_streaming():
    """Example: Stream responses for long-running queries."""
    logger.info("=" * 70)
    logger.info("EXAMPLE 5: Streaming Responses")
    logger.info("=" * 70)
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        ado_org_name=os.getenv("ADO_ORG_NAME"),
    )
    
    try:
        print("\nAgent Response (streaming):\n")
        async for chunk in agent.process_query_stream(
            "Generate a summary report of all work items completed this sprint, "
            "organized by team member and including metrics on velocity"
        ):
            print(chunk, end="", flush=True)
        print("\n")
    finally:
        await agent.cleanup()


async def example_custom_agent():
    """Example: Agent with custom system prompt."""
    logger.info("=" * 70)
    logger.info("EXAMPLE 6: Custom Specialized Agent")
    logger.info("=" * 70)
    
    custom_instructions = """You are a DevOps specialist assistant with access to Azure DevOps tools.
Your role is to help teams:
1. Manage their sprint planning and work items
2. Monitor pipeline health and build status
3. Review pull requests and code quality
4. Track team capacity and workload

Always provide actionable insights and recommendations based on the data.
Be concise but thorough in your analysis."""
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        ado_org_name=os.getenv("ADO_ORG_NAME"),
        agent_name="DevOpsSpecialist",
        instructions=custom_instructions,
    )
    
    try:
        response = await agent.process_query(
            "Give me a health check of our current project: "
            "How many active bugs do we have? What's the build success rate? "
            "Are we on track with our sprint?"
        )
        print(f"\nAgent Response:\n{response}\n")
    finally:
        await agent.cleanup()


async def main():
    """Run all examples."""
    logger.info("Starting Azure DevOps MCP Integration Examples")
    logger.info(f"Using Foundry endpoint: {os.getenv('FOUNDRY_PROJECT_ENDPOINT')}")
    logger.info(f"Using ADO org: {os.getenv('ADO_ORG_NAME')}\n")
    
    try:
        # Note: Examples are disabled by default since they require:
        # 1. Valid Azure credentials (az login)
        # 2. Valid Foundry model deployment
        # 3. Valid Azure DevOps organization with data
        
        # Uncomment to run individual examples:
        # await example_work_items()
        # await example_pull_requests()
        # await example_pipelines()
        # await example_team_capacity()
        # await example_streaming()
        # await example_custom_agent()
        
        logger.info("=" * 70)
        logger.info("MCP Integration Examples Ready")
        logger.info("=" * 70)
        logger.info("\nAvailable examples (uncomment in main() to run):")
        logger.info("  - example_work_items(): Query and manage work items")
        logger.info("  - example_pull_requests(): Manage pull requests")
        logger.info("  - example_pipelines(): Monitor pipelines")
        logger.info("  - example_team_capacity(): Team capacity management")
        logger.info("  - example_streaming(): Stream responses")
        logger.info("  - example_custom_agent(): Custom specialized agent")
        logger.info("\nQueries you can use:")
        logger.info("  - 'List all my open work items in project X'")
        logger.info("  - 'Show me recent pull requests waiting for review'")
        logger.info("  - 'What are the latest pipeline failures?'")
        logger.info("  - 'Create a new bug: [description]'")
        logger.info("  - 'Link work item 123 to pull request 456'")
        logger.info("  - 'Show team capacity for current sprint'")
    
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
