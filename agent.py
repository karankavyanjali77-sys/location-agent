from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
import os

MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:8000/mcp")

def create_agent():
    mcp_toolset = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=MCP_SERVER_URL,
        )
    )
    agent = LlmAgent(
        model="gemini-2.0-flash",
        name="zoo_tour_guide",
        instruction="""You are an expert zoo tour guide. When a user asks about an animal:
        1. Use get_animal_info to fetch structured data from our zoo database
        2. Use get_wikipedia_summary to enrich the response with more context
        3. Combine both into a friendly, informative tour guide response.""",
        tools=[mcp_toolset],
    )
    return agent
