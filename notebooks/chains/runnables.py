
# runnable lambda
from langchain_core.runnables import RunnableLambda
runnable = RunnableLambda(lambda x: x.upper())
result = runnable.invoke("hello")
print(result)
# Output: "HELLO"

# runnable each
from langchain_core.runnables.base import RunnableEach

runnable_each = RunnableEach(bound=RunnableLambda(lambda x: x * 2))
result = runnable_each.invoke([1, 2, 3])
print(result)

# runnable map
from langchain_core.runnables import RunnableMap

# Define each operation to apply to specific inputs
# whole dataframe is given to each runnable lambda during each operation
runnable_map = RunnableMap({
    "double": RunnableLambda(lambda x: x["double"] * 2),
    "square": RunnableLambda(lambda x: x["square"] ** 2),
    "some":RunnableLambda(lambda x:x)
})

result = runnable_map.invoke({"double": 3, "square": 4, "some":5})

print(result)
# Expected Output: 'double': 6, 'square': 16, 'some': {'double': 3, 'square': 4, 'some': 5}}


# runnable sequence
from langchain_core.runnables import RunnableSequence

# Using *steps to define each transformation in sequence
sequence_steps = RunnableSequence(
    RunnableLambda(lambda x: x * 2),       # Step 1: Double the input
    RunnableLambda(lambda x: x + 10),      # Step 2: Add 10
    RunnableLambda(lambda x: x ** 2)       # Step 3: Square the result
)

result_steps = sequence_steps.invoke(3)
print("Result with *steps:", result_steps)  


# Using first, middle, and last to define a sequence
sequence_parts = RunnableSequence(
    first=RunnableLambda(lambda x: x * 2),               # First step
    middle=[RunnableLambda(lambda x: x + 10)],           # Middle steps
    last=RunnableLambda(lambda x: x ** 2)                # Last step
)

result_parts = sequence_parts.invoke(3)
print("Result with first, middle, last:", result_parts) 



# runnable branch
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: x > 0, RunnableLambda(lambda x: "Positive")),
    (lambda x: x < 0, RunnableLambda(lambda x: "Negative")),
    RunnableLambda(lambda x: "Zero")
)

result = branch.invoke(5)
print(result)  # Expected Output: "Positive"

# parallel
from langchain_core.runnables import RunnableParallel
parallel_runnable = RunnableParallel({
    "double": RunnableLambda(lambda x: x * 2),
    "square": RunnableLambda(lambda x: x ** 2)
})
result = parallel_runnable.invoke(3)
print(result)


# runnable retry
from langchain_core.runnables.retry import RunnableRetry

retry_runnable = RunnableRetry(bound=RunnableLambda(lambda x: 1 / x), retries=3,
                                exceptions=(ValueError, ZeroDivisionError), wait_exponential_jitter=True)

try:
    result = retry_runnable.invoke(4)
except Exception as e:
    result = "issue occurred"
print(result)  # Expected Output: "Retry limit exceeded"

# alternate option 
import time

def foo(input) -> None:
    '''Fake function that raises an exception.'''
    raise ValueError(f"Invoking foo failed. At time {time.time()}")

runnable = RunnableLambda(foo)

runnable_with_retries = runnable.with_retry(
    retry_if_exception_type=(ValueError,), # Retry only on ValueError
    wait_exponential_jitter=True, # Add jitter to the exponential backoff
    stop_after_attempt=2, # Try twice
)


try:
    result = runnable_with_retries.invoke(4)
except Exception as e:
    result = "issue occurred"
print(result)  # Expected Output: "Retry limit exceeded"


# The method invocation above is equivalent to the longer form below:

runnable_with_retries = RunnableRetry(
    bound=runnable,
    retry_exception_types=(ValueError,),
    max_attempt_number=2,
    wait_exponential_jitter=True
)




# other runnables
from langchain_core.runnables import Runnable