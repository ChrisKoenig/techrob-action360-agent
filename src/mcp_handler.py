"""MCP (Model Context Protocol) server handler for Azure DevOps."""

import logging
import subprocess
import json
from typing import Any, Dict, Optional, List
from contextlib import asynccontextmanager
import asyncio
import os

logger = logging.getLogger(__name__)


class MCPHandler:
    """Handles connections to Azure DevOps MCP server via stdio."""
    
    def __init__(self, org_name: str):
        """
        Initialize MCP handler for Azure DevOps.
        
        Args:
            org_name: Azure DevOps organization name (e.g., 'UnifiedActionTracker')
        """
        self.org_name = org_name
        self.process: Optional[subprocess.Popen] = None
        self.tools_cache: Dict[str, Any] = {}
        logger.info(f"MCPHandler initialized for Azure DevOps org: {org_name}")
    
    def _build_command(self) -> List[str]:
        """
        Build the command to start the Azure DevOps MCP server.
        
        Returns:
            Command as list of strings for subprocess
        """
        # Using npx to run @azure-devops/mcp with the organization name
        return ["npx", "-y", "@azure-devops/mcp@next", self.org_name]
    
    async def start(self) -> None:
        """Start the MCP server process."""
        try:
            command = self._build_command()
            logger.info(f"Starting MCP server with command: {' '.join(command)}")
            
            self.process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
            
            logger.info("MCP server process started successfully")
        except Exception as e:
            logger.error(f"Failed to start MCP server: {e}")
            raise
    
    async def stop(self) -> None:
        """Stop the MCP server process."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                logger.info("MCP server process terminated")
            except subprocess.TimeoutExpired:
                self.process.kill()
                logger.warning("MCP server process killed (timeout)")
            except Exception as e:
                logger.error(f"Error stopping MCP server: {e}")
            finally:
                self.process = None
    
    async def get_tools(self) -> Dict[str, Any]:
        """
        Retrieve available tools from Azure DevOps MCP server.
        
        Returns:
            Dictionary of available tools and their specifications
        """
        if not self.process:
            await self.start()
        
        # Return cached tools for now - in production, would query MCP server
        # The actual tool discovery happens in the Agent Framework integration
        return self.tools_cache
    
    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Call a tool on the MCP server via Agent Framework.
        
        Note: Actual tool invocation is handled by Agent Framework's MCP integration.
        This method is kept for backwards compatibility.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Tool arguments
            
        Returns:
            Tool result
        """
        logger.info(f"Tool call requested: {tool_name} with args: {kwargs}")
        # Tool invocation is handled by Agent Framework's MCPStdioTool
        return {
            "message": "Use Agent Framework's MCPStdioTool for actual tool invocation",
            "tool": tool_name,
            "args": kwargs,
        }
    
    @asynccontextmanager
    async def managed_connection(self):
        """
        Context manager for MCP server connection.
        
        Usage:
            async with mcp_handler.managed_connection():
                # use mcp_handler
        """
        try:
            await self.start()
            yield self
        finally:
            await self.stop()
