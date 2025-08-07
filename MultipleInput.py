# Step 0: Import required Python types and LangGraph library
from typing import Dict, TypedDict                  # For defining state structure (like TS interfaces)
from langgraph.graph import StateGraph             # Core LangGraph class to build the workflow/graph


# Step 1: Define the structure of the graph's state
# This is similar to creating a TypeScript interface or object shape
class MultiInputAgent(TypedDict):
    name: str      # Input 1: Person's name
    age: str       # Input 2: Person's age (as a string)
    result: str    # Output: Final combined message string


# Step 2: Define a graph node function
# A node is like a function or step in the logic — it receives the state and modifies it
def greeting(state: MultiInputAgent) -> MultiInputAgent:
    # Here, we are accessing the input values from the state
    name = state['name']      # Get the person's name
    age = state['age']        # Get the person's age

    # Combine both inputs to form a final message and save it in the 'result' field
    state['result'] = f"Hi {name}, Your Age is {age}"

    # Return the modified state so it can continue through the graph (or be printed)
    return state


# Step 3: Create a new StateGraph using the MultiInputAgent type
# This tells LangGraph what kind of data will flow through your workflow
graph = StateGraph(MultiInputAgent)


# Step 4: Add the greeting node to the graph
# This node runs the greeting() function above when executed
graph.add_node('MultiInput', greeting)


# Step 5: Define the entry point (start) of the graph
# This tells LangGraph to start with the 'MultiInput' node
graph.set_entry_point('MultiInput')


# Step 6: Define the finish point (end) of the graph
# Since there's only one node, the graph also ends at 'MultiInput'
graph.set_finish_point('MultiInput')


# Step 7: Compile the graph into an executable app
# Think of this as preparing the workflow to run like a complete function
app = graph.compile()


# Step 8: Run the compiled graph by passing initial values for 'name' and 'age'
# This is like calling a function with multiple props/parameters
result = app.invoke({'name': "Hamza", 'age': '23'})


# Step 9: Print the output message from the final result
# The message is stored in the 'result' key of the state
print(result['result'])  # Output: Hi Hamza, Your Age is 23
