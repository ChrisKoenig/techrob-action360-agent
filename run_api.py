#!/usr/bin/env python3
"""Start the TechRob Action360 Agent REST API server."""

import asyncio
import logging
import os
from dotenv import load_dotenv
from src.agent import TechRobAgent
from src.api import AgentAPI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Initialize and start the API server."""
    logger.info("Initializing TechRob Action360 Agent...")
    
    # Create agent
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
    )
    
    # Initialize agent (creates Azure AI client)
    await agent.initialize()
    
    # Create API
    api = AgentAPI(
        agent=agent,
        port=int(os.getenv("API_PORT", 8000)),
        host=os.getenv("API_HOST", "0.0.0.0"),
    )
    
    # Start API server
    try:
        logger.info(f"Starting API server on {api.host}:{api.port}")
        api.run()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        await agent.cleanup()
    except Exception as e:
        logger.error(f"Error starting API: {e}")
        await agent.cleanup()
        raise


if __name__ == "__main__":
    asyncio.run(main())
