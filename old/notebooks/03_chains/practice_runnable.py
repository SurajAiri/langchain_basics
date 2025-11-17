from langchain_core.runnables import RunnableLambda, RunnableMap, RunnableParallel, RunnablePassthrough, RunnableBranch, RunnableSequence

lam = RunnableLambda(lambda x: print(x))
lam.invoke("hi")

data = {"a":32,"b":23,"c":3}

map = RunnableMap({
    "double":RunnableLambda(lambda x: x['a']*2),
    "b*3":RunnableLambda(lambda x: x['b']*3),  
    "c":RunnableLambda(lambda x: x['c'])
})
map.invoke(data)


parallel = RunnableParallel({
    "double":RunnableLambda(lambda x: x['a']*2),
    "b*3":RunnableLambda(lambda x: x['b']*3),  
    "c":RunnableLambda(lambda x: x['c'])
})
parallel.invoke(data)

pt = RunnablePassthrough(lambda x: x)
pt.invoke("HI")

branch = RunnableBranch(
    (lambda x:x > 0,RunnableLambda(lambda x:"Positive")),
    (lambda x:x < 0,RunnableLambda(lambda x: "Negative")),
    RunnableLambda(lambda x: "Zero")
    )
branch.invoke(100)

seq = RunnableSequence(
    RunnableLambda(lambda x: x+10),
    RunnableLambda(lambda x: x+30),
    RunnableLambda(lambda x: x+20),
    RunnableLambda(lambda x: x+11),
)
seq.invoke(0)

seq = RunnableSequence(
   first= RunnableLambda(lambda x: x+10),
   middle=[ RunnableLambda(lambda x: x+30),
    RunnableLambda(lambda x: x+20)],
    last=RunnableLambda(lambda x: x+11),
)
seq.invoke(0)