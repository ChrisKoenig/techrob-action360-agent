#!/usr/bin/env python3
"""Start the TechRob Action360 Agent REST API server."""

import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from src.agent import TechRobAgent
from src.api import AgentAPI

# Load environment variables
load_dotenv()

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "agent.log"

# Clear the log file at startup (truncate, don't append)
log_file.touch(exist_ok=True)
with open(log_file, 'w') as f:
    f.write("")

# Configure logging with both console and file handlers
log_level = os.getenv("LOG_LEVEL", "INFO")
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Root logger
root_logger = logging.getLogger()
root_logger.setLevel(log_level)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
console_formatter = logging.Formatter(log_format)
console_handler.setFormatter(console_formatter)
root_logger.addHandler(console_handler)

# File handler (append mode - ok now since we cleared it)
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(log_level)
file_formatter = logging.Formatter(log_format)
file_handler.setFormatter(file_formatter)
root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)

# Set agent logger to INFO level to see instruction changes
agent_logger = logging.getLogger("src.agent")
agent_logger.setLevel(logging.INFO)


def main():
    """Initialize and start the API server."""
    logger.info("Initializing TechRob Action360 Agent...")
    logger.info(f"[LOG] Logging to file: {log_file.absolute()}")
    
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
