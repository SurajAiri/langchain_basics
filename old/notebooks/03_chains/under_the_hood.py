from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate 
from langchain_core.runnables import RunnableLambda, RunnableSequence


model = OllamaLLM(model='phi3.5')

prompt = PromptTemplate.from_template("System: you are a funny comedian\nHuman: Tell me {count} dad jokes on topic {topic}")

prompt_run = RunnableLambda(lambda x: prompt.format_prompt(**x))
model_run = RunnableLambda(lambda x: model.invoke(x.to_messages()))
parse_run = RunnableLambda(lambda x: x)

chain = RunnableSequence(first=prompt_run,middle=[model_run],last=parse_run)

# chain = prompt | model | StrOutputParser()

res = chain.invoke({'count':3,'topic':'relationship'})
print(res)

