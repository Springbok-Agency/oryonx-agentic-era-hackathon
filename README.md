# Market-Mind: The Agentic Marketing Strategist

An autonomous agent system for generating trend-driven marketing campaigns, built with the Google Agent Development Kit (ADK) for the Agentic Era Hackathon.

## Overview

Market-Mind is an advanced multi-agent system designed to automate the entire lifecycle of a marketing campaign, from initial trend discovery to final creative content generation. It acts as a sophisticated AI marketing strategist that can identify what's currently popular, intelligently match those trends with a given product catalog, and then produce ready-to-use marketing concepts.

This project leverages a hierarchical agent architecture to create a modular, powerful, and autonomous workflow.

Built with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.14.1`

## Features

- **Autonomous End-to-End Workflow**: Manages the entire campaign process with minimal human input
- **Real-Time Trend Analysis**: Utilizes a specialized agent to discover and analyze current market trends
- **Intelligent Product Matching**: Analyzes trend data to find the most relevant products from a catalog to promote
- **Creative Content Generation**: Produces marketing concepts and copy based on the trend and product match
- **Orchestration with Planning**: Powered by a master agent using Gemini 2.5 Pro and a BuiltInPlanner to intelligently reason and execute the workflow

## Architecture

The system is built on a hierarchical agent architecture, with a central master agent orchestrating a team of specialized tools and sub-agents.

### 1. Master Agent (root_agent)
This is the "brain" of the operation. It's a powerful LlmAgent responsible for orchestrating the entire workflow.
- **Model**: gemini-2.5-pro
- **Planner**: BuiltInPlanner to enable multi-step reasoning and planning
- **Role**: To interpret the user's initial request and call its specialized tools in the correct sequence to achieve the goal. It does not perform the tasks itself, but delegates to its tools.

### 2. Tool 1: Trend Watcher (trend_watcher_agent)
This is a self-contained sub-agent whose sole purpose is to identify and analyze current trends. It runs its own internal sequence to find relevant topics and format them for the next step.

### 3. Tool 2: Matchmaker (matchmaker_agent)
This is a function tool that acts as the analytical core. It receives the trend data from the trend_watcher and compares it against a predefined product catalog to find the most commercially relevant matches.

### 4. Tool 3: Product Data Retriever (get_product_data)
This function tool retrieves product information from BigQuery database to provide the matchmaker with available product data.

### 5. Tool 4: Creative Agent (marketing_agent)
This function tool handles the final creative step. It takes the output from the matchmaker—the trend and the matched products—and generates compelling marketing copy and concepts.

## How It Works

The agent operates in a sequential, orchestrated workflow managed by the root_agent:

1. **User Prompt**: The user provides a high-level goal, such as "Find a new marketing angle for our products."
2. **Discover Trends**: The root_agent's planner determines that the first step is to find a trend. It calls the trend_watcher_agent tool.
3. **Get Product Data**: The root_agent calls get_product_data to retrieve available products from BigQuery.
4. **Analyze and Match**: The root_agent takes the trends and product data and passes them to the matchmaker_agent tool. This tool returns a data structure containing the best trend-product matches.
5. **Generate Creative**: The root_agent takes the matched data and passes it to the marketing_agent tool to generate the final campaign ideas.
6. **Final Response**: The generated marketing content is returned to the user as the final answer.

## Project Structure

This project is organized as follows:

```
oryonx-agentic-era-hackathon/
├── app/                          # Core application code
│   ├── agent.py                  # Main orchestrator agent (Market-Mind)
│   ├── trend_watcher_agent.py    # Trend discovery and analysis
│   ├── matchmaker.py             # Product-trend matching logic
│   ├── product_data_retriever.py # BigQuery product data access
│   ├── marketing_creative.py     # Marketing content generation
│   ├── imagen_creative.py        # Image generation capabilities
│   ├── veo_creative.py           # Video generation capabilities
│   └── agent_engine_app.py       # Agent Engine application logic
├── .github/                      # CI/CD pipeline configurations
├── deployment/                   # Infrastructure and deployment scripts
├── notebooks/                    # Jupyter notebooks for prototyping
├── tests/                        # Unit, integration, and load tests
├── Makefile                      # Development commands
├── GEMINI.md                     # AI-assisted development guide
├── CLAUDE.md                     # Claude Code guidance
└── pyproject.toml                # Project dependencies and configuration
```

## Getting Started

### Prerequisites

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)
- **Terraform**: For infrastructure deployment - [Install](https://developer.hashicorp.com/terraform/downloads)
- **make**: Build automation tool - [Install](https://www.gnu.org/software/make/) (pre-installed on most Unix-based systems)
- A Google Cloud project with the necessary APIs enabled
- Authenticated gcloud CLI (`gcloud auth application-default login`)

### Installation

1. Clone the repository
2. Install the required dependencies:


```bash
make install
```

3. Create a `.env` file in the root directory and add your Google Cloud Project ID and other necessary environment variables

### Running the Agent

You can run the agent system using the ADK command-line interface:

**Run in interactive mode:**
```bash
adk run
```
Then, enter a prompt like: "Find a new trend for me"

**Run with a web interface:**
```bash
make playground
```
This will launch a Streamlit web UI where you can interact with the agent.

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `make install`       | Install all required dependencies using uv                                                  |
| `make playground`    | Launch Streamlit interface for testing agent locally and remotely |
| `make backend`       | Deploy agent to Agent Engine |
| `make test`          | Run unit and integration tests                                                              |
| `make lint`          | Run code quality checks (codespell, ruff, mypy)                                             |
| `make setup-dev-env` | Set up development environment resources using Terraform                         |
| `uv run jupyter lab` | Launch Jupyter notebook                                                                     |

For full command options and usage, refer to the [Makefile](Makefile).


## Usage

This template follows a "bring your own agent" approach - you focus on your business logic, and the template handles everything else (UI, infrastructure, deployment, monitoring).

1. **Prototype:** Build your Generative AI Agent using the intro notebooks in `notebooks/` for guidance. Use Vertex AI Evaluation to assess performance.
2. **Integrate:** Import your agent into the app by editing `app/agent.py`.
3. **Test:** Explore your agent functionality using the Streamlit playground with `make playground`. The playground offers features like chat history, user feedback, and various input types, and automatically reloads your agent on code changes.
4. **Deploy:** Set up and initiate the CI/CD pipelines, customizing tests as necessary. Refer to the [deployment section](#deployment) for comprehensive instructions. For streamlined infrastructure deployment, simply run `uvx agent-starter-pack setup-cicd`. Check out the [`agent-starter-pack setup-cicd` CLI command](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html). Currently supports GitHub with both Google Cloud Build and GitHub Actions as CI/CD runners.
5. **Monitor:** Track performance and gather insights using Cloud Logging, Tracing, and the Looker Studio dashboard to iterate on your application.

The project includes a `GEMINI.md` file that provides context for AI tools like Gemini CLI when asking questions about your template.


## Deployment

> **Note:** For a streamlined one-command deployment of the entire CI/CD pipeline and infrastructure using Terraform, you can use the [`agent-starter-pack setup-cicd` CLI command](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html). Currently supports GitHub with both Google Cloud Build and GitHub Actions as CI/CD runners.

### Dev Environment

You can test deployment towards a Dev Environment using the following command:

```bash
gcloud config set project <your-dev-project-id>
make backend
```


The repository includes a Terraform configuration for the setup of the Dev Google Cloud project.
See [deployment/README.md](deployment/README.md) for instructions.

### Production Deployment

The repository includes a Terraform configuration for the setup of a production Google Cloud project. Refer to [deployment/README.md](deployment/README.md) for detailed instructions on how to deploy the infrastructure and application.


## Monitoring and Observability
> You can use [this Looker Studio dashboard](https://lookerstudio.google.com/reporting/46b35167-b38b-4e44-bd37-701ef4307418/page/tEnnC) template for visualizing events being logged in BigQuery. See the "Setup Instructions" tab to getting started.

The application uses OpenTelemetry for comprehensive observability with all events being sent to Google Cloud Trace and Logging for monitoring and to BigQuery for long term storage.

## Key Technologies

- **Google Agent Development Kit (ADK)**
- **Google Gemini 2.5 Pro/Flash**
- **Python 3.10+**
- **BigQuery** for product data storage
- **OpenTelemetry** for observability
