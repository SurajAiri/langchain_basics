from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

model = ChatOllama(model='phi3.5')


# chats = ChatPromptTemplate.from_template("Answer the question in one word. {question}. You will get penalty of $100 for every extra word")

# chats.invoke({"question":"Who is president of nepal?"})

# # res = model.invoke("Who is president of nepal")
# # res.content

# res = model.invoke(chats.format(question='Who is president of nepal?'))
# res.content


messages = [
    SystemMessage("You a person who thinks both positive and negative sides critically before saying anything."),
]

while True:
    user = input(":>> ")
    if user.lower() == "exit":
        break
    messages.append(HumanMessage(user))
    print("B>>",end=' ')
    for chunk in model.stream(messages):
        print( chunk.content, end='', flush=True)
    messages.append(AIMessage(chunk.content))
    print()  # for a new line after the response is complete