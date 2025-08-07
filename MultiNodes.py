# Step 0: Import necessary types and LangGraph library
from typing import TypedDict
from langgraph.graph import StateGraph

# Step 1: Define the shape of your state (like a TypeScript interface or prop object)
class Agent(TypedDict):
    name: str    # Input 1: Name
    age: str     # Input 2: Age
    final: str   # Output: Combined message (generated at the end)


# Step 2: Define your first node (like a function or step)
# This node receives the name — here it doesn't change anything, just passes it through
def firstnode(state: Agent) -> Agent:
    state['name'] = state['name']  # Keep the name as is
    return state


# Step 3: Define your second node (next step in the flow)
# This one handles the age (also just passes it through here)
def secondnode(state: Agent) -> Agent:
    state['age'] = state['age']  # Keep the age as is
    return state


# Step 4: Define the third and final node
# This combines the name and age into a final string (like rendering the final output)
def thirdnode(state: Agent) -> Agent:
    state['final'] = f"{state['name']} , {state['age']}"  # Create a combined result
    return state


# Step 5: Create a new graph using the state definition above
graph = StateGraph(Agent)

# Step 6: Add each node (step) to the graph
graph.add_node('first', firstnode)    # First step
graph.add_node('second', secondnode)  # Second step
graph.add_node('third', thirdnode)    # Third step

# Step 7: Define the starting point (entry point) of the graph
graph.set_entry_point('first')        # Start with 'first'

# Step 8: Define the flow of execution using edges (like function chaining)
graph.add_edge('first', 'second')     # After 'first', go to 'second'
graph.add_edge('second', 'third')     # After 'second', go to 'third'

# Step 9: Define where the graph ends (finish point)
graph.set_finish_point('third')       # End the flow at 'third'

# Step 10: Compile the graph into a runnable application
app = graph.compile()

# Step 11: Invoke the graph with initial input data (like passing props)
result = app.invoke({'name': "hamza", "age": "12"})

# Step 12: Print the final result created by the last node
print(result['final'])  # Output: hamza , 12
