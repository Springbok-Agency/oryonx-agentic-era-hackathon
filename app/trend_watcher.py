from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool, google_search
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters

search_agent = LlmAgent(
    name="search_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful AI assistant designed to provide real-time and accurate information.",
    tools=[google_search],
)

trend_watcher = LlmAgent(
    name="trend_watcher",
    model="gemini-2.5-flash",
    instruction="""You are a helpful AI assistant designed to find the latest trends in the news, including their reasoning and impact. 
First, you find trends, and then you look online for more information about them.",
    """,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uvx",
                    args=["google-news-trends-mcp@latest"],
                ),
                timeout=30.0,
            ),
        ),
        AgentTool(search_agent),
    ],
)
