# MS Foundry Agent-to-Agent Communication

This project demonstrates how to create caller and callee agents in Microsoft Azure AI Foundry with agent-to-agent (A2A) communication capabilities.

## Overview

The script `msfoundry_agent_to_agent.py` shows how to:
- Set up an AIProjectClient to connect to Azure AI Foundry
- Create an A2A connection to enable agent-to-agent calls
- Build a coordinator agent that delegates tasks to a remote agent
- Stream responses from the agent interaction

## Prerequisites

- Python 3.9 or higher
- An Azure subscription with AI Foundry resources provisioned
- Azure CLI authenticated with `az login`
- The following Python packages:
  - `azure-identity`
  - `azure-ai-projects`
  - `python-dotenv`

## Setup

1. **Install dependencies:**
   ```bash
   pip install azure-identity azure-ai-projects python-dotenv
   ```

2. **Configure environment variables:**

   Create a `.env` file in the project root with the following:
   ```
   FOUNDRY_PROJECT_ENDPOINT=https://<resource>.ai.azure.com/api/projects/<project>
   A2A_CONNECTION_NAME=<your-a2a-connection-name>
   AGENT_NAME=<your-agent-name>
   MODEL_DEPLOYMENT=<your-model-deployment-name>
   ```

   Replace the placeholder values with your actual Azure Foundry configuration.

3. **Authenticate with Azure:**
   ```bash
   az login
   ```

## Usage

Run the script:
```bash
python msfoundry_agent_to_agent.py
```

The script will:
1. Create an AIProjectClient connection to your Foundry project
2. Look up the A2A connection configuration
3. Create a caller agent with the A2A tool
4. Send a query to the agent ("What can the secondary agent do?")
5. Stream the response, including any A2A calls made to the remote agent
6. Clean up the created agent version

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FOUNDRY_PROJECT_ENDPOINT` | The endpoint URL of your AI Foundry project |
| `A2A_CONNECTION_NAME` | The name of your A2A connection (configured in Foundry) |
| `AGENT_NAME` | Name of the coordinator agent to create |
| `MODEL_DEPLOYMENT` | Azure OpenAI model deployment name (e.g., "gpt-4") |

## License
NA
