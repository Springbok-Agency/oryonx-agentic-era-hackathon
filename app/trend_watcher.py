from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import AgentTool, google_search
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters

google_trends_agent = LlmAgent(
    name="trends_agent",
    model="gemini-2.5-flash",
    instruction="""You are an AI assistant that finds and reports on the latest weekly trends.

Your response MUST strictly follow this format for each trend, including the trend name and its search volume.

## REQUIRED OUTPUT FORMAT:
- **[Trend Name]** ([Number of searches])

## EXAMPLE:
- **Antifa** (2000+ searches)
- **Jimmy Fallon** (500+ searches)
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
    ],
)

google_search_agent = LlmAgent(
    name="search_agent",
    model="gemini-2.5-flash",
    instruction="""You are a specialized AI assistant that receives a trending topic and explains WHY it's trending.

## INSTRUCTIONS:
1.  You will be given a trend's name and its search volume as input.
2.  Use the `Google Search` tool with the trend's name to find the most recent news, articles, or social media discussions related to it.
3.  Synthesize the search results into a concise, one-paragraph summary that explains the key reasons for the trend.
4.  Begin the summary with the trend name in bold, but DO NOT include the search volume in your final output.

## EXAMPLE:
If your input is `- **Jimmy Fallon** (500+ searches)`, your output should be:

**Jimmy Fallon**: The American late-night host is trending amidst news of the cancellation of "Jimmy Kimmel Live!" and former President Trump's call for NBC to also axe "The Tonight Show Starring Jimmy Fallon." Additionally, Fallon is set to be the next guest on the "New Heights" podcast.
""",
    tools=[google_search],
)

output_formatter_agent = LlmAgent(
    name="output_formatter_agent",
    model="gemini-2.5-flash",
    instruction="""You are an expert AI assistant that strictly formats unstructured data into a predefined JSON structure.

## CONSTRAINTS:
- Your output MUST be a valid JSON array of objects.
- Each object in the array represents a single trend.
- Do NOT add any introductory text, explanations, or markdown code fences (e.g., ```json) around the output. Your response must be the raw JSON string only.

## JSON SCHEMA:
The output must be an array `[]` containing objects with the following keys:
- `trend_title`: (string) A concise and compelling title for the trend.
- `trend_description`: (string) A 1-2 sentence summary explaining the trend and its significance.
- `trend_category`: (string) A relevant category for the trend (e.g., "Technology", "Health", "Business", "Culture").

## EXAMPLE:
Here is an example of the expected output format for two trends:
```json
[
  {
    "trend_title": "Antifa",
    "trend_description": "The term is trending in the Netherlands in connection with the assassination of conservative activist Charlie Kirk, as Dutch activist Eva Vlaardingerbroek's commentary brings the group into the local political focus.",
    "trend_category": "Politics",
    "trend_search_volume": "2000+"
  },
  {
    "trend_title": "Jimmy Fallon",
    "trend_description": "The late-night host is trending due to former President Trump's call to cancel his show, a scheduled podcast appearance, and his name being mentioned in discussions surrounding political violence.",
    "trend_category": "Entertainment",
    "trend_search_volume": "500+"
  }
]
""",
)

trend_watcher = SequentialAgent(
    name="trend_watcher",
    sub_agents=[
        google_trends_agent,
        google_search_agent,
        output_formatter_agent,
    ],
)

