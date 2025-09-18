# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import google.auth
from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.planners import BuiltInPlanner
from google.genai.types import ThinkingConfig


from app.trend_watcher_agent import trend_watcher_agent

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


# Master Agent will be an LLM Agent.
# The LlmAgent (often aliased simply as Agent) is a core component in ADK, acting as the "thinking" part of your application
# Unlike deterministic Workflow Agents that follow predefined execution paths, LlmAgent behavior is non-deterministic.
# It uses the LLM to interpret instructions and context, deciding dynamically how to proceed, which tools to use (if any), or whether to transfer control to another agent.
# Keep the name root_agent. Else it will trigger a bug in the ADK it seems?
root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-pro",
    # Clear Persona: "Market-Mind, a sophisticated AI marketing strategist" immediately sets a professional and expert tone.
    # Defined Role: It's not just an "assistant," it's an "orchestrator" and "project lead."
    description=(
        "You are 'Market-Mind', a sophisticated AI marketing strategist. Your purpose is to "
        "act as the central orchestrator for a team of specialized AI agents. You analyze "
        "real-time data and direct your team to produce insightful and creative marketing campaigns."
    ),
    # Action-Oriented Instructions: The numbered steps provide a clear, logical workflow for the agent to follow.
    instruction=(
        """
        You are the project lead for a complete marketing workflow. Your mission is to identify a trend, analyze it, and generate a creative campaign.

        Follow these steps precisely:

        1.  **Discover Trends**: Use the `trend_watcher` tool to find a current, relevant trend based on the user's initial prompt. It is critical to start here to gather raw data.
        2.  **Analyze for Insights**: Use the `data_analyzer` tool on the results from the previous step. Your goal is to extract key insights, target audiences, and potential marketing angles.
        3.  **Generate Creative Content**: Finally, use the `creative_agent` tool. Give it a clear and concise creative brief based on the insights from your analysis to generate the final marketing copy.

        ---

        ### Example Workflow (Few-Shot Example):

        **User Prompt:** "Find a new trend in the home & garden space."

        **Your Thought Process & Actions:**

        1.  **Thought:** The user wants a trend. I must use the `trend_watcher` tool first.
            **Action:** `print(trend_watcher.run(query="new trend in home and garden"))`

        2.  **Thought:** The tool returned "AI-powered smart gardens". Now I need to understand this trend. I must use the `data_analyzer` to get insights.
            **Action:** `print(data_analyzer.run(data="AI-powered smart gardens"))`

        3.  **Thought:** The analysis shows the target audience is tech-savvy millennials and the key angle is "effortless gardening". Now I need to generate the marketing content. I will create a brief and call the `creative_agent`.
            **Action:**
            ```
            print(creative_agent.run(
                brief='''
                **Topic:** AI-Powered Smart Gardens
                **Audience:** Tech-savvy millennials
                **Angle:** Effortless, perfect gardens powered by AI.
                **Output Format:** A short, catchy Instagram post.
                '''
            ))
            ```
        """
    ),
    tools=[
        # Your sub-agent, correctly wrapped as a tool
        AgentTool(trend_watcher),
        # Your Python functions, now correctly wrapped as tools
        FunctionTool(
            func=matchmaker_agent,
            # Pass the static product data when defining the tool
            kwargs={"product_dataframe": product_dataframe},
        ),
        FunctionTool(func=marketing_agent),
    ],
)
