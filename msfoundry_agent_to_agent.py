from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, A2APreviewTool
from dotenv import load_dotenv

load_dotenv() 
# ---- Configuration ----
# Format: "https://<resource>.ai.azure.com/api/projects/<project>"
PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
A2A_CONNECTION_NAME = os.environ["A2A_CONNECTION_NAME"]
AGENT_NAME = os.environ["AGENT_NAME"]
MODEL_DEPLOYMENT = os.environ["MODEL_DEPLOYMENT"]

# ---- Create clients ----
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# ---- Look up the A2A connection (points at the remote/callee agent) ----
a2a_connection = project.connections.get(A2A_CONNECTION_NAME)

a2a_tool = A2APreviewTool(
    project_connection_id=a2a_connection.id,
)

# ---- Create the caller agent, equipped with the A2A tool ----
agent = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=MODEL_DEPLOYMENT,
        instructions=(
            "You are a coordinator agent. When the user's question requires "
            "specialized knowledge, delegate it to the connected remote agent "
            "via the A2A tool, then summarize its answer for the user."
        ),
        tools=[a2a_tool],
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

# ---- Call the caller agent, which in turn calls the remote agent ----
user_input = "What can the secondary agent do?"

stream_response = openai.responses.create(
    stream=True,
    tool_choice="required",  # force the model to use the A2A tool
    input=user_input,
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

for event in stream_response:
    if event.type == "response.created":
        print(f"Response created (id: {event.response.id})")
    elif event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "response.output_item.done":
        item = event.item
        if getattr(item, "type", None) == "remote_function_call":
            # This fires when the caller agent invokes the remote (A2A) agent
            print(f"\n[A2A call] call_id={getattr(item, 'call_id', None)} "
                  f"label={getattr(item, 'label', None)}")
    elif event.type == "response.completed":
        print(f"\n\nFinal answer:\n{event.response.output_text}")

# ---- Clean up the agent version created for this demo ----
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)