from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate 

model = OllamaLLM(model='phi3.5')

prompt = PromptTemplate.from_template("System: you are a funny comedian\nHuman: Tell me {count} dad jokes on topic {topic}")

chain = prompt | model | StrOutputParser()

res = chain.invoke({'count':3,'topic':'relationship'})
print(res)
