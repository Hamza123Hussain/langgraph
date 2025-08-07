# 1. Import necessary types for type hinting
from typing import Dict, TypedDict

# 2. Import the main class for creating a graph
from langgraph.graph import StateGraph

# 3. Define a custom type (schema) for the agent's state
class AgentState(TypedDict):
    message: str  # The state will carry a string under the key 'message'

# 4. Define a node (function) in the graph
def greetingnode(state: AgentState) -> AgentState:
    # Update the message in the state with a greeting
    state['message'] = 'Hey ' + state['message'] + ', how are you doing '
    
    # Return the updated state
    return state

# 5. Initialize a new state graph with the AgentState type
graph = StateGraph(AgentState)

# 6. Add a node to the graph
# The node is called 'greeter', and it's the function `greetingnode`
graph.add_node('greeter', greetingnode)

# 7. Set the starting point of the graph to be the 'greeter' node
graph.set_entry_point('greeter')

# 8. Since we only have one node, also make it the finish point
graph.set_finish_point('greeter')

# 9. Compile the graph into an executable application
app = graph.compile()

# 10. Invoke the compiled app with an initial state where message is "Bob"
result = app.invoke({'message': "Bob"})

# 11. Print the final message from the result
print(result["message"])  # Output: Hey Bob, how are you doing 
