#!/usr/bin/env python3
"""Simple example of using TechRob Action360 Agent with Foundry GPT-4o."""

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


async def simple_query_example():
    """Example: Simple query to the agent."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 1: Simple Query")
    logger.info("=" * 60)
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
    )
    
    try:
        response = await agent.process_query("What is the capital of France?")
        print(f"\nAgent Response:\n{response}\n")
    finally:
        await agent.cleanup()


async def streaming_query_example():
    """Example: Streaming query to the agent."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 2: Streaming Query")
    logger.info("=" * 60)
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
    )
    
    try:
        print("\nAgent Response (streaming):\n")
        async for chunk in agent.process_query_stream("Write a short poem about technology"):
            print(chunk, end="", flush=True)
        print("\n")
    finally:
        await agent.cleanup()


async def custom_instructions_example():
    """Example: Agent with custom instructions."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 3: Agent with Custom Instructions")
    logger.info("=" * 60)
    
    custom_instructions = """You are a technical expert specializing in cloud infrastructure.
You provide concise, technical responses with specific details and best practices.
Format your responses with clear sections when appropriate."""
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        agent_name="TechExpertAgent",
        instructions=custom_instructions,
    )
    
    try:
        response = await agent.process_query("What are the benefits of microservices architecture?")
        print(f"\nAgent Response:\n{response}\n")
    finally:
        await agent.cleanup()


async def main():
    """Run all examples."""
    logger.info("Starting TechRob Action360 Agent Examples")
    logger.info(f"Using Foundry endpoint: {os.getenv('FOUNDRY_PROJECT_ENDPOINT')}")
    logger.info(f"Model deployment: {os.getenv('MODEL_DEPLOYMENT')}\n")
    
    try:
        # Run examples
        await simple_query_example()
        await streaming_query_example()
        await custom_instructions_example()
        
        logger.info("=" * 60)
        logger.info("All examples completed successfully!")
        logger.info("=" * 60)
    
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
