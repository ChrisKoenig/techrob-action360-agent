"""Configuration models using Pydantic."""

from pydantic import BaseModel, Field
from typing import Optional


class FoundryConfig(BaseModel):
    """Microsoft Foundry configuration."""
    
    project_name: str = Field(..., description="Foundry project name")
    resource_group: str = Field(..., description="Azure resource group")
    subscription_id: str = Field(..., description="Azure subscription ID")
    model_name: str = Field(default="gpt-4o", description="Model name")
    model_deployment: str = Field(default="gpt-4o", description="Model deployment name")
    
    class Config:
        env_prefix = "FOUNDRY_"


class MCPConfig(BaseModel):
    """MCP Server configuration."""
    
    server_url: str = Field(default="http://localhost:3000", description="MCP server URL")
    server_type: str = Field(default="stdio", description="MCP server type (stdio or http)")
    server_command: Optional[str] = Field(default=None, description="Command to start MCP server")
    
    class Config:
        env_prefix = "MCP_"


class APIConfig(BaseModel):
    """REST API configuration."""
    
    port: int = Field(default=8000, description="API port")
    host: str = Field(default="0.0.0.0", description="API host")
    
    class Config:
        env_prefix = "API_"


class AgentConfig(BaseModel):
    """Agent configuration."""
    
    name: str = Field(default="TechRob Action360 Agent", description="Agent name")
    description: str = Field(default="Multi-platform AI agent", description="Agent description")
    system_prompt: Optional[str] = Field(default=None, description="System prompt for the agent")
    
    foundry: FoundryConfig
    mcp: MCPConfig
    api: APIConfig
    
    class Config:
        env_nested_delimiter = "__"
