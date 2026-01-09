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


def main():
    """Initialize and start the API server."""
    logger.info("Initializing TechRob Action360 Agent...")
    
    # Create agent (don't initialize yet - it will initialize on first query)
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        ado_org_name=os.getenv("ADO_ORG_NAME", "UnifiedActionTracker"),
        ado_project_name=os.getenv("ADO_PROJECT_NAME", "Unified Action Tracker"),
    )
    
    # Create API
    api = AgentAPI(
        agent=agent,
        port=int(os.getenv("API_PORT", 8000)),
        host=os.getenv("API_HOST", "0.0.0.0"),
    )
    
    # Start API server
    try:
        logger.info(f"Starting API server on {api.host}:{api.port}")
        logger.info("Available endpoints:")
        logger.info("  POST /api/query - Send a query to the agent")
        logger.info("  POST /api/query/stream - Stream agent response (Server-Sent Events)")
        logger.info("  GET /api/health - Health check")
        logger.info("  GET /api/tools - List available tools")
        api.run()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error starting API: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
