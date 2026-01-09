"""Tests for the agent."""

import pytest
from src.agent import TechRobAgent


@pytest.mark.asyncio
async def test_process_query():
    """Test processing a simple query."""
    agent = TechRobAgent()
    response = await agent.process_query("Hello agent")
    assert response is not None
    assert "Processed" in response


def test_agent_initialization():
    """Test agent initialization."""
    agent = TechRobAgent()
    assert agent is not None
    assert agent.get_available_tools() == {}
