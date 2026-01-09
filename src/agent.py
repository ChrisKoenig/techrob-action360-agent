"""Core agent implementation using Microsoft Agent Framework."""

import logging
import os
from typing import Optional, AsyncGenerator
from azure.identity.aio import DefaultAzureCredential
from agent_framework.azure import AzureAIClient
from agent_framework import MCPStdioTool

logger = logging.getLogger(__name__)


class TechRobAgent:
    """TechRob Action360 AI Agent with Foundry GPT-4o and Azure DevOps MCP integration."""
    
    def __init__(
        self,
        project_endpoint: Optional[str] = None,
        model_deployment_name: Optional[str] = None,
        ado_org_name: Optional[str] = None,
        ado_project_name: Optional[str] = None,
        agent_name: str = "TechRobAction360Agent",
        instructions: Optional[str] = None,
        enable_mcp: bool = True,
    ):
        """
        Initialize the agent with Foundry credentials and MCP tools.
        
        Args:
            project_endpoint: Azure AI Foundry project endpoint. Defaults to env var.
            model_deployment_name: Model deployment name. Defaults to env var.
            ado_org_name: Azure DevOps organization name. Defaults to env var.
            ado_project_name: Azure DevOps project name. Defaults to env var.
            agent_name: Name of the agent.
            instructions: System instructions for the agent.
            enable_mcp: Whether to enable Azure DevOps MCP tools.
        """
        self.project_endpoint = project_endpoint or os.getenv("FOUNDRY_PROJECT_ENDPOINT")
        self.model_deployment_name = model_deployment_name or os.getenv("MODEL_DEPLOYMENT", "gpt-4o")
        self.ado_org_name = ado_org_name or os.getenv("ADO_ORG_NAME", "UnifiedActionTracker")
        self.ado_project_name = ado_project_name or os.getenv("ADO_PROJECT_NAME", "Unified Action Tracker")
        self.agent_name = agent_name
        self.enable_mcp = enable_mcp
        
        default_instructions = f"""You are TechRob Action360, a helpful AI assistant with access to Azure DevOps tools.
You work with the Azure DevOps organization '{self.ado_org_name}' and the project '{self.ado_project_name}'.
You can help users manage work items, pull requests, pipelines, and team capacity.
You have access to Azure DevOps via the MCP server, which provides tools for:
- Creating and managing work items (tasks, bugs, features)
- Managing pull requests and code review
- Viewing pipeline runs and build status
- Team iterations and capacity planning
- Repository management

Always provide clear, accurate, and concise responses.
When users ask about Azure DevOps data, use the appropriate tools to fetch real data from the '{self.ado_project_name}' project."""
        
        self.instructions = instructions or default_instructions
        self.credential = None
        self.client = None
        self.agent = None
        self.mcp_tools = []
        
        logger.info(f"TechRobAgent initialized (name={agent_name}, endpoint={self.project_endpoint}, ADO org={self.ado_org_name})")
    
    def _create_mcp_tools(self) -> list:
        """
        Create MCP tool instances for Azure DevOps.
        
        Returns:
            List of MCP tool instances
        """
        if not self.enable_mcp:
            return []
        
        try:
            tools = [
                MCPStdioTool(
                    name="Azure DevOps MCP",
                    description="Access Azure DevOps work items, pull requests, pipelines, and team management tools",
                    command="npx",
                    args=[
                        "-y",
                        "@azure-devops/mcp@next",
                        self.ado_org_name,
                    ],
                    load_prompts=False,
                )
            ]
            logger.info(f"Created {len(tools)} MCP tool(s)")
            return tools
        except Exception as e:
            logger.error(f"Failed to create MCP tools: {e}")
            return []
    
    async def initialize(self) -> None:
        """
        Initialize Azure AI client and agent.
        Must be called before using the agent.
        """
        try:
            self.credential = DefaultAzureCredential()
            self.client = AzureAIClient(
                project_endpoint=self.project_endpoint,
                model_deployment_name=self.model_deployment_name,
                credential=self.credential,
            )
            
            # Create MCP tools if enabled
            self.mcp_tools = self._create_mcp_tools()
            
            logger.info("Azure AI Client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure AI Client: {e}")
            raise
    
    async def cleanup(self) -> None:
        """Clean up resources."""
        if self.credential:
            await self.credential.close()
        logger.info("Agent cleanup completed")
    
    async def process_query(self, query: str) -> str:
        """
        Process a user query and return a response.
        
        Args:
            query: User query string
            
        Returns:
            Agent response string
        """
        if not self.client:
            await self.initialize()
        
        logger.info(f"Processing query: {query}")
        
        try:
            async with self.client.create_agent(
                name=self.agent_name,
                instructions=self.instructions,
                tools=self.mcp_tools,  # Include MCP tools
            ) as agent:
                result = await agent.run(query)
                return result.text if result.text else "No response generated"
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise
    
    async def process_query_stream(self, query: str) -> AsyncGenerator[str, None]:
        """
        Process a user query and stream the response.
        
        Args:
            query: User query string
            
        Yields:
            Response text chunks
        """
        if not self.client:
            await self.initialize()
        
        logger.info(f"Processing query (streaming): {query}")
        
        try:
            async with self.client.create_agent(
                name=self.agent_name,
                instructions=self.instructions,
                tools=self.mcp_tools,  # Include MCP tools
            ) as agent:
                async for chunk in agent.run_stream(query):
                    if chunk.text:
                        yield chunk.text
        except Exception as e:
            logger.error(f"Error streaming query: {e}")
            raise
    
    def get_available_tools(self) -> dict:
        """
        Get available tools (MCP tools and system capabilities).
        
        Returns:
            Dictionary of available tools
        """
        return {
            "mcp_tools": len(self.mcp_tools),
            "mcp_enabled": self.enable_mcp,
            "ado_org": self.ado_org_name,
            "capabilities": [
                "work_items",
                "pull_requests", 
                "pipelines",
                "repositories",
                "team_capacity",
                "iterations",
            ],
        }
