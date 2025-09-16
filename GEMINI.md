# GEMINI.md

## Project Overview

This project is a command-line tool that integrates with Gemini to provide AI-powered assistance for various development tasks. It allows users to interact with Gemini for code reviews, issue triage, and general AI assistance directly from the terminal. The project appears to be a Node.js application that utilizes the Gemini API.

## Building and Running

**TODO:** The commands for building, running, and testing the project are not explicitly defined in the project files. This section should be updated with the correct commands once they are known.

### Installation

```bash
# TODO: Add installation commands
```

### Running the application

```bash
# TODO: Add commands to run the application
```

### Testing

```bash
# TODO: Add commands to run tests
```

## CI/CD

This project uses GitHub Actions for CI/CD. The main workflow is `.github/workflows/gemini-dispatch.yml`, which is triggered by various GitHub events such as pull request reviews, comments, and issue creation. Based on the event and the command in the comment (e.g., `@gemini-cli /review`, `@gemini-cli /triage`), it dispatches the appropriate workflow.

### Workflows

*   **`gemini-dispatch.yml`**: The main entry point for all Gemini-related actions. It listens to GitHub events and dispatches the appropriate workflow.
*   **`gemini-review.yml`**: This workflow automatically reviews pull requests using Gemini. It can be triggered automatically when a pull request is opened or manually by commenting `@gemini-cli /review` on a pull request.
*   **`gemini-triage.yml`**: This workflow automatically triages issues using Gemini. It can be triggered automatically when an issue is opened or manually by commenting `@gemini-cli /triage` on an issue. This workflow uses Gemini to analyze the issue and apply appropriate labels.
*   **`gemini-invoke.yml`**: This workflow is a general-purpose AI assistant that can perform a wide range of tasks, including creating branches, updating files, and creating pull requests. It is triggered by the `gemini-dispatch.yml` workflow when a user invokes the Gemini CLI with a general command (e.g., `@gemini-cli explain this code`).
*   **`gemini-scheduled-triage.yml`**: This workflow runs on a schedule (every hour) to find untriaged issues (issues with no labels or with the `status/needs-triage` label) and apply appropriate labels using Gemini.

## Development Conventions

*   **Environment Variables:** The project requires a `.env` file with a `GOOGLE_CLOUD_PROJECT` variable for authentication with the Gemini API.
*   **Dependencies:** The project uses Node.js, and dependencies are likely managed via npm or yarn, as indicated by the presence of `node_modules` in the `.gitignore` file.
