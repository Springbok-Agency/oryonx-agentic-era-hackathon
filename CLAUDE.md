# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the "Social Pulse Agent" - an AI-powered social media monitoring and marketing automation tool built with Google's Agent Development Kit (ADK). The main goal is to automatically discover trending topics, match them with relevant products, and create compelling marketing campaigns including Instagram posts with images, videos, and hashtags.

## Architecture

The project follows a multi-agent architecture using Google ADK:

- **Root Agent** (`app/agent.py`): The main orchestrator "Market-Mind" that coordinates specialized agents
- **Trend Watcher Agent** (`app/trend_watcher_agent.py`): Discovers current trending topics and news
- **Matchmaker Agent** (`app/matchmaker.py`): Finds creative connections between trends and products
- **Product Data Retriever** (`app/product_data_retriever.py`): Retrieves product information from BigQuery
- **Marketing Creative Agent** (`app/marketing_creative.py`): Generates marketing content
- **Imagen Creative** (`app/imagen_creative.py`): Handles image generation
- **Veo Creative** (`app/veo_creative.py`): Handles video generation

The root agent automatically executes a workflow: discover trends → get product data → match & analyze → present results.

## Development Commands

| Command | Description |
|---------|-------------|
| `make install` | Install all dependencies using uv package manager |
| `make playground` | Launch Streamlit interface for local testing with hot-reload |
| `make backend` | Deploy agent to Agent Engine |
| `make test` | Run unit and integration tests (`pytest tests/unit && pytest tests/integration`) |
| `make lint` | Run code quality checks (codespell, ruff format/check, mypy) |
| `make setup-dev-env` | Set up development environment resources using Terraform |
| `uv run jupyter lab` | Launch Jupyter notebook for prototyping |

## Technology Stack

- **Framework**: Google Agent Development Kit (ADK) v1.8.0
- **Python**: >=3.10,<=3.14
- **Package Manager**: uv (required for all dependency management)
- **LLM**: Gemini 2.5 Pro/Flash models via Vertex AI
- **Data**: BigQuery for product data storage
- **Testing**: pytest with asyncio support
- **Linting**: ruff, mypy, codespell
- **Deployment**: Google Cloud (Agent Engine, Cloud Run)

## Code Style & Standards

- Uses ruff for code formatting and linting with 88-character line length
- Type hints required (mypy enforced)
- AsyncIO patterns throughout
- Agent-based architecture with clear separation of concerns
- Each agent has a specific role and set of tools

## Testing Strategy

- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- Load tests in `tests/load_test/`
- Agent evaluation supported via `.evalset.json` files
- Use `pytest` with async support for testing agent workflows

## Environment Setup

- Requires Google Cloud authentication via `gcloud auth application-default login`
- Environment variables: `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `GOOGLE_GENAI_USE_VERTEXAI`
- Uses Vertex AI for Gemini models in production

## Agent Configuration Notes

- The root agent is configured with built-in planning and safety settings
- Uses AgentTool wrappers for sub-agents and FunctionTool for utility functions
- Temperature set to 0.2 for deterministic but creative output
- Max output tokens limited to 250 for concise responses
- Comprehensive safety filters enabled for all harm categories