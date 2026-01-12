"""Core agent implementation using Microsoft Agent Framework."""

import logging
import os
from pathlib import Path
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
        instruction_type: str = "summary",
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
            instructions: System instructions for the agent. If provided, overrides instruction_type.
            instruction_type: Type of instructions to load ("summary", "routing", etc.). Defaults to "summary".
            enable_mcp: Whether to enable Azure DevOps MCP tools.
        """
        self.project_endpoint = project_endpoint or os.getenv("FOUNDRY_PROJECT_ENDPOINT")
        self.model_deployment_name = model_deployment_name or os.getenv("MODEL_DEPLOYMENT", "gpt-4o")
        self.ado_org_name = ado_org_name or os.getenv("ADO_ORG_NAME", "UnifiedActionTracker")
        self.ado_project_name = ado_project_name or os.getenv("ADO_PROJECT_NAME", "Unified Action Tracker")
        self.agent_name = agent_name
        self.enable_mcp = enable_mcp
        self.instruction_type = instruction_type
        
        # Load instructions from file if not provided
        if instructions:
            self.instructions = instructions
        else:
            self.instructions = self._load_instructions(instruction_type=instruction_type)
        
        self.credential = None
        self.client = None
        self.agent = None
        self.mcp_tools = []
        
        logger.info(f"[INIT] TechRobAgent initialized (name={agent_name}, ADO org={self.ado_org_name}, instruction_type={instruction_type})")
    
    def _load_instructions(self, instruction_type: str = "summary") -> str:
        """
        Load instructions from config/instructions_<type>.md file.
        Falls back to default instructions if file not found.
        
        Args:
            instruction_type: Type of instructions to load ("summary", "routing", etc.)
                             Defaults to "summary"
        
        Returns:
            Instructions string for the agent
        """
        # Try specific instruction file first
        instructions_path = Path(__file__).parent.parent / "config" / f"instructions_{instruction_type}.md"
        
        if instructions_path.exists():
            try:
                with open(instructions_path, 'r', encoding='utf-8') as f:
                    instructions = f.read()
                logger.info(f"Loaded instructions from {instructions_path}")
                return instructions
            except Exception as e:
                logger.warning(f"Failed to load instructions from file: {e}, trying fallback")
        
        # Try legacy instructions.md for backward compatibility
        legacy_instructions_path = Path(__file__).parent.parent / "config" / "instructions.md"
        if legacy_instructions_path.exists():
            try:
                with open(legacy_instructions_path, 'r', encoding='utf-8') as f:
                    instructions = f.read()
                logger.info(f"Loaded instructions from {legacy_instructions_path} (legacy)")
                return instructions
            except Exception as e:
                logger.warning(f"Failed to load legacy instructions from file: {e}, using default")
        
        # Fallback to default instructions
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
        return default_instructions
    
    def set_instruction_type(self, instruction_type: str) -> None:
        """
        Dynamically change the instruction set for the agent.
        
        Args:
            instruction_type: Type of instructions to load ("summary", "routing", etc.)
        """
        logger.info(f"[SWITCH] set_instruction_type: {self.instruction_type} -> {instruction_type}")
        self.instruction_type = instruction_type
        self.instructions = self._load_instructions(instruction_type=instruction_type)
        logger.info(f"[OK] Instructions changed to: {instruction_type} (loaded {len(self.instructions)} chars)")
    
    def _create_mcp_tools(self) -> list:
        """
        Create MCP tool instances for Azure DevOps.
        
        Returns:
            List of MCP tool instances
        """
        if not self.enable_mcp:
            return []
        
        try:
            # Build MCP command arguments
            # The Azure DevOps MCP server accepts: org_name [project_name]
            mcp_args = [
                "-y",
                "@azure-devops/mcp@next",
                self.ado_org_name,
            ]
            
            # Add project name if available - this helps MCP server set the correct project context
            if self.ado_project_name:
                mcp_args.append(self.ado_project_name)
                logger.info(f"[MCP] Using project: {self.ado_project_name}")
            
            tools = [
                MCPStdioTool(
                    name="Azure DevOps MCP",
                    description="Access Azure DevOps work items, pull requests, pipelines, and team management tools",
                    command="npx",
                    args=mcp_args,
                    load_prompts=True,  # Enable this so LLM knows how to use the tools
                )
            ]
            logger.info(f"[MCP] Created {len(tools)} tool(s)")
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
            logger.info(f"[OK] Created {len(self.mcp_tools)} MCP tool(s)")
            for tool in self.mcp_tools:
                logger.info(f"  - Tool: {tool.name}")
                logger.info(f"    Description: {tool.description}")
            
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
        logger.info(f"Using instruction type: {self.instruction_type}")
        logger.info(f"MCP Tools available: {len(self.mcp_tools)}")
        for tool in self.mcp_tools:
            logger.info(f"  - {tool.name}")
        logger.info("=" * 80)
        logger.info("INSTRUCTIONS BEING USED:")
        logger.info("=" * 80)
        logger.info(self.instructions)
        logger.info("=" * 80)
        
        try:
            # Create agent with MCP tools registered
            async with self.client.create_agent(
                name=self.agent_name,
                instructions=self.instructions,
                tools=self.mcp_tools if self.mcp_tools else None,  # Pass tools to agent
            ) as agent:
                logger.info(f"[RUN] Agent created. Running query: '{query}' (len={len(query)})")
                result = await agent.run(query)
                logger.info(f"[OK] Agent response received ({len(result.text) if result.text else 0} chars)")
                if result.text:
                    logger.debug(f"Response preview: {result.text[:500]}...")
                return result.text if result.text else "No response generated"
        except TypeError as e:
            # If create_agent doesn't accept tools, try without it
            if "tools" in str(e):
                logger.warning(f"Agent framework doesn't accept tools parameter, attempting without: {e}")
                async with self.client.create_agent(
                    name=self.agent_name,
                    instructions=self.instructions,
                ) as agent:
                    # Try to set tools directly on agent
                    if hasattr(agent, 'tools'):
                        agent.tools = self.mcp_tools
                    result = await agent.run(query)
                    return result.text if result.text else "No response generated"
            else:
                raise
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
