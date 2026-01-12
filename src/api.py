"""REST API for multi-platform agent access."""

import logging
import os
from typing import Dict, Any
from aiohttp import web
from src.agent import TechRobAgent

logger = logging.getLogger(__name__)


class AgentAPI:
    """REST API for accessing the agent."""
    
    def __init__(self, agent: TechRobAgent, port: int = 8000, host: str = "0.0.0.0"):
        """
        Initialize the API.
        
        Args:
            agent: TechRobAgent instance
            port: Port to run the API on
            host: Host to bind to
        """
        self.agent = agent
        self.port = port or int(os.getenv("API_PORT", 8000))
        self.host = host or os.getenv("API_HOST", "0.0.0.0")
        self.app = web.Application()
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up API routes."""
        self.app.router.add_post('/api/query', self.query_handler)
        self.app.router.add_post('/api/query/stream', self.query_stream_handler)
        self.app.router.add_get('/api/health', self.health_handler)
        self.app.router.add_get('/api/tools', self.tools_handler)
    
    async def query_handler(self, request: web.Request) -> web.Response:
        """
        Handle query requests (non-streaming).
        
        Expected JSON body: {"query": "user question", "instruction_type": "summary"}
        
        Args:
            request: HTTP request with JSON body
            - query (required): The user query string
            - instruction_type (optional): Type of instructions to use ("summary", "routing", etc.)
                                          Defaults to "summary"
        """
        try:
            data = await request.json()
            query = data.get('query')
            instruction_type = data.get('instruction_type', 'summary')
            
            if not query:
                return web.json_response(
                    {'error': 'query field is required'},
                    status=400
                )
            
            # Switch instruction type if provided and different from current
            if instruction_type != self.agent.instruction_type:
                logger.info(f"Switching instruction type from '{self.agent.instruction_type}' to '{instruction_type}'")
                self.agent.set_instruction_type(instruction_type)
            
            response = await self.agent.process_query(query)
            
            return web.json_response({
                'query': query,
                'instruction_type': instruction_type,
                'response': response
            })
        
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return web.json_response(
                {'error': str(e)},
                status=500
            )
    
    async def query_stream_handler(self, request: web.Request) -> web.StreamResponse:
        """
        Handle streaming query requests.
        
        Expected JSON body: {"query": "user question", "instruction_type": "summary"}
        Streams back Server-Sent Events (SSE) format.
        
        Args:
            request: HTTP request with JSON body
            - query (required): The user query string
            - instruction_type (optional): Type of instructions to use ("summary", "routing", etc.)
                                          Defaults to "summary"
        """
        try:
            data = await request.json()
            query = data.get('query')
            instruction_type = data.get('instruction_type', 'summary')
            
            if not query:
                return web.json_response(
                    {'error': 'query field is required'},
                    status=400
                )
            
            response = web.StreamResponse()
            response.content_type = 'text/event-stream'
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['X-Accel-Buffering'] = 'no'
            await response.prepare(request)
            
            # Switch instruction type if provided and different from current
            if instruction_type != self.agent.instruction_type:
                logger.info(f"Switching instruction type from '{self.agent.instruction_type}' to '{instruction_type}'")
                self.agent.set_instruction_type(instruction_type)
            
            logger.info(f"Starting stream for query: {query} (instruction_type: {instruction_type})")
            
            async for chunk in self.agent.process_query_stream(query):
                event = f"data: {chunk}\n\n"
                await response.write(event.encode('utf-8'))
            
            await response.write_eof()
            return response
        
        except Exception as e:
            logger.error(f"Error streaming query: {e}")
            return web.json_response(
                {'error': str(e)},
                status=500
            )
    
    async def health_handler(self, request: web.Request) -> web.Response:
        """Health check endpoint."""
        return web.json_response({'status': 'healthy'})
    
    async def tools_handler(self, request: web.Request) -> web.Response:
        """Get available tools and current configuration."""
        tools = self.agent.get_available_tools()
        return web.json_response({
            'tools': tools,
            'current_instruction_type': self.agent.instruction_type,
            'supported_instruction_types': ['summary', 'routing']
        })
    
    async def run_async(self):
        """Start the API server asynchronously."""
        logger.info(f"Starting API on {self.host}:{self.port}")
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        logger.info(f"API server started on http://{self.host}:{self.port}")
        return runner
    
    def run(self):
        """Start the API server (synchronous)."""
        logger.info(f"Starting API on {self.host}:{self.port}")
        web.run_app(self.app, host=self.host, port=self.port)


if __name__ == '__main__':
    import asyncio
    
    agent = TechRobAgent()
    api = AgentAPI(agent)
    api.run()
