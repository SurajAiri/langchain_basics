from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI


load_dotenv()


# custom tools:
def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    import datetime  # Import datetime module to get current time

    now = datetime.datetime.now()  # Get current time
    return now.strftime("%I:%M %p")  # Format time in H:MM AM/PM format


# create tools
tools = [
    Tool(
        name="Current Time",  # Name of the tool
        func=get_current_time,  # Function that the tool will execute
        description="Useful for when you need to know the current time",  # Description of the tool
    )
]

# model and prompt for creating agent
prompt = hub.pull("hwchase17/react")
llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0
)

# create agent
agent = create_react_agent(
    llm=llm, 
    tools=tools,
    prompt=prompt,
    # stop_sequence=["\n\n"], # Stop sequence when the agent encounters a stop token
)

# create agent executor
executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
)

# run agent
res = executor.invoke({"input": "What time is it?"})
print(res)