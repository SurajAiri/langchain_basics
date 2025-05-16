import dotenv
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
)
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
dotenv.load_dotenv()

# define custom tool (function): to get current time

def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    import datetime  # Import datetime module to get current time

    now = datetime.datetime.now()  # Get current time
    return now.strftime("%I:%M %p")  # Format time in H:MM AM/PM format

# List of tools available to the agent
tools = [
    Tool(
        name="Current Time",  # Name of the tool
        func=get_current_time,  # Function that the tool will execute
        description="Useful for when you need to know the current time",  # Description of the tool
    ),
]   

# Pull the prompt template from the hub
# ReAct = Reason and Action
# https://smith.langchain.com/hub/hwchase17/react
prompt = hub.pull("hwchase17/react")

# Initialize a ChatOpenAI model
llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0
)

# Create the ReAct agent using the create_react_agent function: ReAct = Reason and Action
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    # stop_sequence=["\n\n"], # Stop sequence when the agent encounters a stop token
)

# Create an agent executor from the agent and tools
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
)

# Run the agent with a test query
response = agent_executor.invoke({"input": "What time is it?"})
print("response:", response)