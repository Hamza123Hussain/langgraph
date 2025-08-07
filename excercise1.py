# Importing necessary types from Python's type system
from typing import Dict, TypedDict

# Importing the main class to create a state-based graph
from langgraph.graph import StateGraph

# Step 1: Define the structure (or "schema") of the data flowing through the graph
# This is similar to creating an interface or object shape in TypeScript
class ComplimentAgent(TypedDict):
    name: str  # The state will carry a "name" as a string


# Step 2: Create a "node" (function) which represents one step of your graph
# Think of this like a function or a component that updates the state
def greeting(state: ComplimentAgent) -> ComplimentAgent:
    # Modify the 'name' field by appending a compliment string
    state['name'] = state['name'] + ', you are doing an amazing job learning LangGraph'
    
    # Return the updated state back to the graph
    return state


# Step 3: Initialize a new graph that will use our defined state structure
graph = StateGraph(ComplimentAgent)

# Step 4: Add a node to the graph
# This node is called 'Compliment' and it runs the `greeting` function when called
graph.add_node('Compliment', greeting)

# Step 5: Set the starting point of the graph
# This means the graph should begin execution from the 'Compliment' node
graph.set_entry_point('Compliment')

# Step 6: Set the finishing point of the graph
# Since we only have one node, it will also be the last one to run
graph.set_finish_point('Compliment')

# Step 7: Compile the graph
# This prepares the graph so it can be executed — like building a workflow
app = graph.compile()

# Step 8: Call (invoke) the compiled graph with an initial input
# This is like calling a function and passing props or parameters
result = app.invoke({'name': "Hamza"})

# Step 9: Print the final result — specifically the updated 'name' field
print(result['name'])  # Output: Hamza, you are doing an amazing job learning LangGraph
