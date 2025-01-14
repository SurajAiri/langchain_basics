LangChain’s **runnables** offer modular and flexible components to define and compose custom data processing steps in workflows. Here’s a list of LangChain runnables, including their syntax, purpose, and example usage cases:

### 1. `RunnableLambda`

- **Purpose**: Executes a lambda function, typically used for quick transformations or operations.
- **Syntax**:
  ```python
  from langchain_core.runnables import RunnableLambda
  runnable = RunnableLambda(lambda x: x.upper())
  result = runnable.invoke("hello")
  print(result)
  # Output: "HELLO"
  ```
- **Use Case**: Transforming text (e.g., converting to uppercase), formatting outputs, or applying any simple one-line transformation.

### 2. `RunnableEach`

- **Purpose**: Applies the same runnable to each item in a list. This is useful for iterating over and processing lists.
- **Syntax**:
  ```python
  from langchain_core.runnables import RunnableLambda
  from langchain_core.runnables.base import RunnableEach

  runnable_each = RunnableEach(bound=RunnableLambda(lambda x: x * 2))
  result = runnable_each.invoke([1, 2, 3])
  print(result)
  ```
- **Use Case**: Processing lists where each item needs the same operation (e.g., formatting each element, adding prefixes, etc.).

### 3. `RunnableMap`

- **Purpose**: Applies different runnables to each key-value pair in a dictionary, useful for tasks where each key has specific processing needs.
- **Syntax**:
  ```python
  from langchain_core.runnables import RunnableMap, RunnableLambda

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
  ```
- **Use Case**: Processing dictionaries where different keys require different transformations (e.g., calculations on multiple metrics, data parsing).

### 4. `RunnableSequence`

- **Purpose**: Runs multiple runnables in a sequence, passing the output of one as the input to the next.
- **Syntax**:
  ```python
  from langchain_core.runnables import RunnableSequence, RunnableLambda

  # Using *steps to define each transformation in sequence
  sequence_steps = RunnableSequence(
      RunnableLambda(lambda x: x * 2),       # Step 1: Double the input
      RunnableLambda(lambda x: x + 10),      # Step 2: Add 10
      RunnableLambda(lambda x: x ** 2)       # Step 3: Square the result
  )

  result_steps = sequence_steps.invoke(3)
  print("Result with *steps:", result_steps)  
  #OUTPUT: Result with *steps: 256


  # Using first, middle, and last to define a sequence
  sequence_parts = RunnableSequence(
      first=RunnableLambda(lambda x: x * 2),               # First step
      middle=[RunnableLambda(lambda x: x + 10)],           # Middle steps
      last=RunnableLambda(lambda x: x ** 2)                # Last step
  )

  result_parts = sequence_parts.invoke(3)
  print("Result with first, middle, last:", result_parts) 
  # OUTPUT: Result with first, middle, last: 256
  ```
- **Use Case**: Chaining transformations (e.g., preprocessing, followed by a transformation, and ending with validation).

### 5. `RunnableBranch`

- **Purpose**: Executes one of several runnables based on a condition. Each condition directs the flow to a specific runnable.
- **Syntax**:
  ```python
  from langchain_core.runnables import RunnableBranch,RunnableLambda
  branch = RunnableBranch(
      (lambda x: x > 0, RunnableLambda(lambda x: "Positive")),
      (lambda x: x < 0, RunnableLambda(lambda x: "Negative")),
      RunnableLambda(lambda x: "Zero")
  )
  result = branch.invoke(5)
  print(result)  # Expected Output: "Positive"

  ```
- **Use Case**: Decision-making in workflows where a choice depends on input (e.g., categorizing text based on sentiment, filtering based on conditions).

### 6. `RunnableParallel`

- **Purpose**: Executes multiple runnables in parallel, combining their results into a dictionary output.
- **Syntax**:
  ```python
  from langchain_core.runnables import RunnableParallel, RunnableLambda
  parallel_runnable = RunnableParallel({
      "double": RunnableLambda(lambda x: x * 2),
      "square": RunnableLambda(lambda x: x ** 2)
  })
  result = parallel_runnable.invoke(3)
  print(result)
  #OUTPUT: {'double': 6, 'square': 9}
  ```
- **Use Case**: Running independent tasks in parallel, useful for performance optimization (e.g., processing multiple attributes simultaneously or combining different data insights).

### 7. `RunnableRetry`

- **Purpose**: Retries a runnable if it encounters an error or fails, with optional retry logic and error handling.
- **Syntax**:
  ```python
  from langchain_core.runnables.retry import RunnableRetry

  runnable_with_retries = RunnableRetry(
      bound=runnable,
      retry_exception_types=(ValueError,),
      max_attempt_number=3,
      wait_exponential_jitter=True
  )
  # Output: Retries 3 times and raises an error if it fails
  ```
- **Use Case**: Error handling in unreliable or external calls (e.g., API requests with intermittent connectivity issues, retrying unstable network tasks).

### 8. `RunnablePassThrough`
- **Purpose** no-op runnable that passes the input directly to the output without any changes.

- **Syntax**
  ```python
  from langchain_core.runnables import RunnablePassthrough

  passthrough = RunnablePassthrough()
  result = passthrough.invoke("Some input")
  print(result)
  #OUTPUT: Some input
  ```
- **Use Case**: Debugging or testing pipelines without transformations, Placeholders in a pipeline

### Summary Table

| Runnable                | Purpose                                                            | Use Case Example                          |
| ----------------------- | ------------------------------------------------------------------ | ----------------------------------------- |
| **RunnableLambda**      | Executes a simple lambda function.                                 | Text transformation, formatting.          |
| **RunnableEach**        | Applies a runnable to each item in a list.                         | Processing list items.                    |
| **RunnableMap**         | Processes dictionary key-value pairs with specific runnables.      | Processing dict attributes differently.   |
| **RunnableSequence**    | Runs multiple runnables in a specified order.                      | Chaining transformations.                 |
| **RunnableBranch**      | Chooses a runnable to execute based on conditions.                 | Conditional task routing.                 |
| **RunnableParallel**    | Runs multiple runnables in parallel.                               | Running independent tasks concurrently.   |
| **RunnableRetry**       | Retries a runnable if it fails, with optional error handling.      | External API calls with potential errors. |
| **RunnablePassthrough** | Passes input to output unchanged.                                  | Debugging or testing pipelines.           |

---

<br>

| **Runnable**            | **Description**                           | **Use Case**                                   | **When to Use**                              | **When to Avoid**                              |
|-------------------------|-------------------------------------------|-----------------------------------------------|---------------------------------------------|------------------------------------------------|
| **RunnableLambda**      | Wraps a custom Python function.           | Custom lightweight processing.                | Small, reusable logic.                      | Complex or domain-specific tasks.              |
| **RunnableEach**        | Applies a task to each list item.         | Batch processing.                             | Independent list items.                     | Dependent list items or very large lists.      |
| **RunnableMap**         | Runs tasks concurrently.                  | Parallel independent tasks.                   | Independent tasks needing grouped output.   | Dependent tasks.                               |
| **RunnableSequence**    | Chains tasks sequentially.                | Linear workflows.                             | Linear task dependencies.                   | Parallelizable tasks.                          |
| **RunnableBranch**      | Executes tasks conditionally.             | Conditional workflows.                        | Input-dependent logic.                      | Overly complex or unclear branching.           |
| **RunnableParallel**    | Runs tasks in parallel and combines outputs. | Concurrently executed tasks with merging results. | Combining results from independent tasks.  | Tasks requiring strict execution order.        |
| **RunnableRetry**       | Retries tasks on failure.                 | Transient error recovery.                     | Prone-to-fail operations.                   | Deterministic failures.                        |
| **RunnablePassthrough** | Passes input to output unchanged.         | Debugging or placeholders.                    | Debugging or development.                   | Production pipelines without use.              |

---

