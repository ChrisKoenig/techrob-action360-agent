"""Core agent implementation using Microsoft Agent Framework."""

import logging
import os
from typing import Optional, AsyncGenerator
from azure.identity.aio import DefaultAzureCredential
from agent_framework.azure import AzureAIClient

logger = logging.getLogger(__name__)


class TechRobAgent:
    """TechRob Action360 AI Agent with Foundry GPT-4o."""
    
    def __init__(
        self,
        project_endpoint: Optional[str] = None,
        model_deployment_name: Optional[str] = None,
        agent_name: str = "TechRobAction360Agent",
        instructions: Optional[str] = None,
    ):
        """
        Initialize the agent with Foundry credentials.
        
        Args:
            project_endpoint: Azure AI Foundry project endpoint. Defaults to env var.
            model_deployment_name: Model deployment name. Defaults to env var.
            agent_name: Name of the agent.
            instructions: System instructions for the agent.
        """
        self.project_endpoint = project_endpoint or os.getenv("FOUNDRY_PROJECT_ENDPOINT")
        self.model_deployment_name = model_deployment_name or os.getenv("MODEL_DEPLOYMENT", "gpt-4o")
        self.agent_name = agent_name
        
        default_instructions = """You are TechRob Action360, a helpful AI assistant.
You provide clear, accurate, and concise responses to user queries.
You analyze data and provide insights to help users make informed decisions."""
        
        self.instructions = instructions or default_instructions
        self.credential = None
        self.client = None
        self.agent = None
        
        logger.info(f"TechRobAgent initialized (name={agent_name}, endpoint={self.project_endpoint})")
    
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
            ) as agent:
                async for chunk in agent.run_stream(query):
                    if chunk.text:
                        yield chunk.text
        except Exception as e:
            logger.error(f"Error streaming query: {e}")
            raise
    
    def get_available_tools(self) -> dict:
        """
        Get available tools (placeholder for future MCP integration).
        
        Returns:
            Dictionary of available tools
        """
        return {}
