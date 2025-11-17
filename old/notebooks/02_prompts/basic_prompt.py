
#--------------------------------------------------------
# PromptTemplate
#--------------------------------------------------------
from langchain.prompts import PromptTemplate
# Define a template with placeholders
template = "Translate the following English text to French: {text}"

# Create a PromptTemplate
prompt = PromptTemplate(
    input_variables=["text"],  # The placeholders in the template
    template=template
)
# Use the prompt
input_text = "How are you?"
filled_prompt = prompt.format(text=input_text)
print(filled_prompt)


#--------------------------------------------------------
# ChatPromptTemplate
#--------------------------------------------------------
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage

# Define message templates
system_message = SystemMessagePromptTemplate.from_template("You are a helpful assistant.")
human_message = HumanMessagePromptTemplate.from_template("Can you help me with {task}?")

# Create a ChatPromptTemplate
chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])

# Use the prompt
filled_prompt = chat_prompt.format(task="understanding LangChain prompts")
print(filled_prompt)

# ----------------------------------------------------------
# msgs = [
#     ("system","you are a critical thinker"),
#     ("human","what does life mean?")
# ]
# prompts = ChatPromptTemplate.from_messages(msgs)
# prompts.format()

# # variant 2
# msgs = [
#     ("system","you are a critical thinker"),
#     ("human","Answer this question in one word. {question}")
# ]
# prompts = ChatPromptTemplate.from_messages(msgs)
# prompts.format(question='What is 2 plus 2 equals to')

# variant 3 -> this doesn't work it will not replace {question}
msgs = [
    ("system","you are a critical thinker"),
    HumanMessage("Answer this question in one word. {question}")
]
prompts = ChatPromptTemplate.from_messages(msgs)
prompts.format(question='What is 2 plus 2 equals to')

# variant 4 (rather do this for variant 3 issue or variant 2 is easier option)
msgs = [
    ("system","you are a critical thinker"),
    HumanMessagePromptTemplate.from_template("Answer this question in one word. {question}")
]
prompts = ChatPromptTemplate.from_messages(msgs)
prompts.format(question='What is 2 plus 2 equals to')



#--------------------------------------------------------
# FewShotPromptTemplate
#--------------------------------------------------------

from langchain.prompts import FewShotPromptTemplate, PromptTemplate

# Define examples
examples = [
    {"input": "Hello", "output": "Bonjour"},
    {"input": "Goodbye", "output": "Au revoir"}
]

# Define example template
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}"
)

# Create FewShotPromptTemplate
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Translate the following English text to French:",
    suffix="Input: {text}\nOutput:",
    input_variables=["text"]
)

# Use the prompt
filled_prompt = few_shot_prompt.format(text="How are you?")
print(filled_prompt)
