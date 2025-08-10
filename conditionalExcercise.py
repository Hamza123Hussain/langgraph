# Step 0: Import required types and LangGraph components
from typing import TypedDict
from langgraph.graph import StateGraph, START, END  # START and END are special nodes for graph flow


# Step 1: Define the shape of the state (like an interface in TypeScript)
class AgentState(TypedDict):
    number1: int        # First number
    operation: str      # Operation symbol: "+" or "-"
    number2: int        # Second number
    finalNumber: int    # The result after performing the operation
    number3:int
    number4:int
    operation2:str
    finalNumber2:int


# Step 2: Define a node that adds two numbers
def adder(state: AgentState) -> AgentState:
    """This node adds the two numbers and stores the result."""
    state["finalNumber"] = state["number1"] + state["number2"]
    return state


# Step 3: Define a node that subtracts two numbers
def subtractor(state: AgentState) -> AgentState:
    """This node subtracts the second number from the first."""
    state["finalNumber"] = state["number1"] - state["number2"]
    return state

# Step 2: Define a node that multipication two numbers
def mul(state: AgentState) -> AgentState:
    """This node adds the two numbers and stores the result."""
    state["finalNumber2"] = state["number3"] * state["number4"]
    return state
# Step 2: Define a node that multipication two numbers
def div(state: AgentState) -> AgentState:
    """This node adds the two numbers and stores the result."""
    state["finalNumber2"] = state["number3"] / state["number4"]
    return state

# Step 4: Define a decision-making function
# Instead of modifying state, this one chooses the NEXT node in the flow
def decide_next_node(state: AgentState) -> str:
    """This function decides which node should run next based on the operation."""
    if state["operation"] == "+":
        return "addition_operation"       # We'll map this name to the "add_node"
    elif state["operation"] == "-":
        return "subtraction_operation" 


def decide_next_node2(state: AgentState) -> str:
    if state["operation2"] == "*":
        return "multipication_operation"       # We'll map this name to the "add_node"
    elif state["operation2"] == "/":
        return "division_operation"  # We'll map this name to the "subtract_node"
# Step 5: Create the graph
graph = StateGraph(AgentState)


# Step 6: Add the main calculation nodes
graph.add_node("add_node", adder)         # Node for addition
graph.add_node("subtract_node", subtractor)  # Node for subtraction

graph.add_node('mulnode',mul)
graph.add_node('divnode',div)

# Step 7: Add a "router" node that just passes state forward
# This acts like a hub where we decide the path to take
graph.add_node("router", lambda state: state)

graph.add_node('router2',lambda state:state)

# Step 8: Define the starting point of the graph
graph.add_edge(START, "router")  # The first step after START is always "router"


# Step 9: Add conditional edges from the router
# The flow from "router" will depend on what decide_next_node() returns
graph.add_conditional_edges(
    "router",             # From node
    decide_next_node,     # Function to decide path
    {
        # Mapping of decision string -> actual graph node
        "addition_operation": "add_node",
        "subtraction_operation": "subtract_node"
    }
)


# Step 10: Define where the graph ends
graph.add_edge("add_node",'router2')       # After addition, go to END
graph.add_edge("subtract_node", 'router2')  # After subtraction, go to END


graph.add_conditional_edges(
    'router2',decide_next_node2,{
        'multipication_operation':"mulnode","division_operation":"divnode"
    }
)

graph.add_edge('mulnode',END)
graph.add_edge('divnode',END)
# Step 11: Compile the graph into a runnable application
app = graph.compile()


# Step 12: Run the graph with initial input
# Here we tell it to do subtraction: 10 - 5
result = app.invoke({"number1": 30, "operation": "+", "number2": 5,'number3':7,'number4':2,"operation2":"*"})

# Step 13: Output the result
print(result)  # Output: {'number1': 10, 'operation': '-', 'number2': 5, 'finalNumber': 5}
