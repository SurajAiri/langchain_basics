from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.tools import Tool,tool
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from googlesearch import search
from serpapi import GoogleSearch
import os


@tool
def search_google(query):
    """Searches Google and returns the first valid search result using SerpAPI."""
    try:
        print(f"[DEBUG] Tool 'Google Search' called with query: {query}")
        params = {
            "q": query,
            "api_key": os.environ.get("SERP_API_KEY"),
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        if "organic_results" in results and results["organic_results"]:
            top_result = results["organic_results"][0]["link"]
            print("our result: ", top_result)
            return top_result

        return "No results found."

    except Exception as e:
        return f"I couldn't find any information on that. Error: {e}"



load_dotenv()


# custom tools:
@tool
def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    import datetime  # Import datetime module to get current time

    now = datetime.datetime.now()  # Get current time
    return now.strftime("%I:%M %p")  # Format time in H:MM AM/PM format
@tool
def search_wikipedia(query):
    """Searches Wikipedia and returns the summary of the first result."""
    from wikipedia import summary

    try:
        return summary(query, sentences=2) # Limit to two sentences for brevity
    except:
        return "I couldn't find any information on that."

@tool
def search_google(query):
    """Searches Google and returns the first valid result."""
    try:
        print(f"[DEBUG] Tool 'Google Search' called with query: {query}")
        results = list(search(query, num_results=3))

        # Filter out empty strings and unwanted results
        filtered_results = [url for url in results if url.strip()]

        if not filtered_results:
            return "No valid results found."

        print("our result: ", filtered_results)
        return filtered_results[0]  # Return the first valid result

    except Exception as e:
        return f"I couldn't find any information on that. Error: {e}"


# create tools
tools = [
    # Tool(
    #     name="Current Time",  # Name of the tool
    #     func=get_current_time,  # Function that the tool will execute
    #     description="Useful for when you need to know the current time",  # Description of the tool
    # ),
    Tool(
        name="Wikipedia",
        func=search_wikipedia,
        description="Provides general knowledge and historical information about well-known topics. Does NOT include the latest updates or real-time news.",
    ),
    Tool(
        name="Google Search",
        func=search_google,
        description="Finds the latest updates, real-time news, and information not covered by Wikipedia. Use this for fresh, trending, or time-sensitive topics.",
    )
]


# model and prompt for creating agent

# Load the correct JSON Chat Prompt from the hub
prompt = hub.pull("hwchase17/structured-chat-agent")

# Initialize a ChatOpenAI model
llm = ChatOpenAI(model="gpt-4o-mini")

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
    memory=memory, # use memory to store conversation history and maintain context
    handle_parsing_errors=True, # handle parsing errors
)


# run agent
# Initial system message to set the context for the chat
# SystemMessage is used to define a message from the system to the agent, setting initial instructions or context
initial_message = "You are an AI assistant that can provide helpful answers using available tools.\nIf you are unable to answer, you can use the following tools:  Google Search."
memory.chat_memory.add_message(SystemMessage(content=initial_message))


# Chat Loop to interact with the user
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    # Add the user's message to the conversation memory
    memory.chat_memory.add_message(HumanMessage(content=user_input))

    # Invoke the agent with the user input and the current chat history
    response = agent_executor.invoke({"input": user_input})
    print("Bot:", response["output"])

    # Add the agent's response to the conversation memory
    memory.chat_memory.add_message(AIMessage(content=response["output"]))