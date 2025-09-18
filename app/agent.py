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
from google.adk.planners import BuiltInPlanner
from google.adk.tools import AgentTool, FunctionTool
from google.genai import types
from google.genai.types import ThinkingConfig

from app.matchmaker import matchmaker_agent
from app.product_data_retriever import get_product_data
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
        "You are 'Market-Mind', a sophisticated AI marketing strategist specializing in trend analysis "
        "and product marketing. Your purpose is to discover trending topics, match them with relevant "
        "products, and create compelling marketing campaigns. You orchestrate a team of specialized "
        "agents to deliver data-driven marketing insights and creative content."
    ),
    # Action-Oriented Instructions: The numbered steps provide a clear, logical workflow for the agent to follow.
    instruction=(
        """
        You are Market-Mind, an autonomous marketing strategist. When given ANY request, you MUST immediately start executing the full workflow without asking questions or waiting for confirmation.

        ## MANDATORY IMMEDIATE ACTIONS:
        Upon receiving any user input, you must IMMEDIATELY call these tools:

        1. FIRST: Call `trend_watcher_agent` with query "find current trending topics"
        2. SIMULTANEOUSLY: Call `get_product_data` to retrieve available products
        3. THEN: Call `matchmaker_agent` with the trend and product data to find matches
        4. FINALLY: Present complete marketing insights

        ## CRITICAL RULES:
        - NEVER ask "Would you like me to..." or "Should I start by..."
        - NEVER wait for user confirmation
        - IMMEDIATELY start with tool calls upon any user input
        - Execute the complete workflow every time
        - Think through your plan, then ACT immediately

        ## Tools Available:
        - `trend_watcher_agent`: Call with basic query like "find current trends"
        - `get_product_data`: Call with no parameters to get all products
        - `matchmaker_agent`: Call with trends and products data as JSON strings

        Your role is to be PROACTIVE and AUTONOMOUS. Start working immediately!
        """
    ),
    tools=[
        AgentTool(trend_watcher_agent),
        # FunctionTool(func=get_product_data),
        # FunctionTool(func=matchmaker_agent),
        # FunctionTool(func=marketing_agent),
        get_product_data,
        matchmaker_agent,
    ],
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(
            include_thoughts=True,  # Include the agent's internal thoughts in the output for transparency
            thinking_budget=1024,  # Limit the number of tokens/thoughts the agent can use for reasoning
        )
    ),
    generate_content_config=types.GenerateContentConfig(
        # High values are creative, low values are deterministic
        temperature=0.2,
        # Increase this if we want more detailed output.
        max_output_tokens=250,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
        ],
    ),
)
