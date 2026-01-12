#!/usr/bin/env python3
"""
Example: Using Dynamic Instructions with TechRob Action360 Agent

This example demonstrates how to switch between different instruction sets
(summary, routing, etc.) to get different types of analysis from the same agent.
"""

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


async def example_summary_mode():
    """Example 1: Get a summary of an Action."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 1: Summary Mode")
    logger.info("=" * 60)
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        instruction_type="summary",  # Explicitly set to summary mode
    )
    
    try:
        query = "Show me action 12345 with all details"
        logger.info(f"\nQuery: {query}")
        response = await agent.process_query(query)
        print(f"\nAgent Response (Summary Mode):\n{response}\n")
    finally:
        await agent.cleanup()


async def example_routing_mode():
    """Example 2: Get routing recommendations for an Action."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 2: Routing Mode")
    logger.info("=" * 60)
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        instruction_type="routing",  # Set to routing mode
    )
    
    try:
        query = "Analyze action 12345 and provide routing recommendation"
        logger.info(f"\nQuery: {query}")
        response = await agent.process_query(query)
        print(f"\nAgent Response (Routing Mode):\n{response}\n")
    finally:
        await agent.cleanup()


async def example_dynamic_switch():
    """Example 3: Dynamically switch instructions within same agent."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 3: Dynamic Instruction Switching")
    logger.info("=" * 60)
    
    # Create agent with summary mode
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        instruction_type="summary",
    )
    
    try:
        # Query 1: Summary
        logger.info("\nStep 1: Get summary of action 12345")
        query1 = "Show me action 12345"
        response1 = await agent.process_query(query1)
        print(f"Summary Response:\n{response1}\n")
        
        # Switch instructions dynamically
        logger.info("\nStep 2: Switch to routing mode")
        agent.set_instruction_type("routing")
        logger.info(f"Current instruction type: {agent.instruction_type}")
        
        # Query 2: Routing recommendation
        logger.info("\nStep 3: Get routing recommendation for same action")
        query2 = "Now analyze this action for routing and provide recommendations"
        response2 = await agent.process_query(query2)
        print(f"Routing Response:\n{response2}\n")
        
        # Switch back to summary
        logger.info("\nStep 4: Switch back to summary mode")
        agent.set_instruction_type("summary")
        
    finally:
        await agent.cleanup()


async def example_streaming_with_routing():
    """Example 4: Stream routing recommendations."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 4: Streaming with Routing Instructions")
    logger.info("=" * 60)
    
    agent = TechRobAgent(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model_deployment_name=os.getenv("MODEL_DEPLOYMENT", "gpt-4o"),
        instruction_type="routing",
    )
    
    try:
        query = "Analyze action 12345 and provide detailed routing recommendation"
        logger.info(f"\nQuery: {query}")
        logger.info("Streaming response (routing mode):\n")
        
        async for chunk in agent.process_query_stream(query):
            print(chunk, end="", flush=True)
        print("\n")
        
    finally:
        await agent.cleanup()


async def main():
    """Run all examples."""
    logger.info("\n" + "=" * 60)
    logger.info("TechRob Action360: Dynamic Instructions Examples")
    logger.info("=" * 60)
    logger.info("\nThese examples show how to use different instruction sets")
    logger.info("for different types of analysis (summary vs routing).\n")
    
    # Choose which examples to run
    # Uncomment to run specific examples
    
    await example_summary_mode()
    # await example_routing_mode()
    # await example_dynamic_switch()
    # await example_streaming_with_routing()


if __name__ == "__main__":
    asyncio.run(main())
