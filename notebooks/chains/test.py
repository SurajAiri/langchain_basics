from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()
result = passthrough.invoke("Some input")
print(result)
#OUTPUT: Some input