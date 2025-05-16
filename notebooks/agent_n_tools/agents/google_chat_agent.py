from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from googlesearch import search


load_dotenv()

# custom tools:
def google_search(query: str):
    """Searches Google and returns the summary of the first result."""
    try:
        print(f"[DEBUG] Tool 'Google Search' called with query: {query}")
        results = list(search(query, num_results=1))
        return results[0] if results else "No results found."
    except Exception as e:
        return f"I couldn't find any information on that. Error: {e}"

# Define argument schema for the tool
class GoogleSearchArgs(BaseModel):
    query: str

# tools creation
tools = [
    StructuredTool(
        name="Google Search",  # Name of the tool
        func=google_search,  # Function that the tool will execute
        description="Useful for when you need to search for information on Google",  # Description of the tool
        args_schema=GoogleSearchArgs,  # Argument schema for the tool
    ),
]

# model and prompt for creating agent

# Load the correct JSON Chat Prompt from the hub
prompt = hub.pull("hwchase17/structured-chat-agent")

# Initialize a ChatGoogleGenerativeAI model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite-preview-02-05")

# Create a structured Chat Agent with Conversation Buffer Memory
# ConversationBufferMemory stores the conversation history, allowing the agent to maintain context across interactions
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)

# create_structured_chat_agent initializes a chat agent designed to interact using a structured prompt and tools
# It combines the language model (llm), tools, and prompt to create an interactive agent
agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)

# create agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,  # use memory to store conversation history and maintain context
    handle_parsing_errors=True,  # handle parsing errors
)

# run agent
# Initial system message to set the context for the chat
# SystemMessage is used to define a message from the system to the agent, setting initial instructions or context
initial_message = "You are an AI assistant that can provide helpful answers using available tools.\nIf you are unable to answer, you can use the following tools: Google Search."
memory.chat_memory.add_message(SystemMessage(content=initial_message))

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break
    
    # Add user message to memory
    memory.chat_memory.add_message(HumanMessage(content=user_input))

    # Invoke the agent with the current chat history
    response = agent_executor.invoke({"input": user_input})
    print("Bot:", response["output"])

    # Add the bot response to memory
    memory.chat_memory.add_message(AIMessage(content=response["output"]))
