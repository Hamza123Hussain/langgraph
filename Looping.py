from langgraph.graph import StateGraph, END
import random
from typing import List, TypedDict

# Step 1: Define the shape of the state
class AgentState(TypedDict):
    name: str         # Person's name
    number: List[int] # List of generated numbers
    counter: int      # How many numbers have been generated so far


# Step 2: First node — greeting
def greeting_node(state: AgentState) -> AgentState:
    """Greeting node: say hi and reset counter."""
    state["name"] = f"Hi there, {state['name']}"  # ✅ fixed string formatting
    state["counter"] = 0  # Start counting from zero
    return state


# Step 3: Second node — generate a random number
def random_node(state: AgentState) -> AgentState:
    """Generates a random number between 0 and 10, adds to list, increments counter."""
    state["number"].append(random.randint(0, 10))
    state["counter"] += 1
    return state


# Step 4: Decision node — decide whether to loop or exit
def should_continue(state: AgentState) -> str:
    """Returns 'loop' to continue generating numbers, or 'exit' to finish."""
    if state["counter"] < 5:
        print("ENTERING LOOP", state["counter"])
        return "loop"
    else:
        return "exit"


# Step 5: Build the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)

# Connect greeting → random
graph.add_edge("greeting", "random")

# Conditional edges: after random_node, decide whether to loop or exit
graph.add_conditional_edges(
    "random",
    should_continue,
    {
        "loop": "random",  # Keep looping back to random_node
        "exit": END        # Stop the graph
    }
)

# Set entry point
graph.set_entry_point("greeting")

# Step 6: Compile and run
app = graph.compile()

result = app.invoke({"name": "Vaibhav", "number": [], "counter": 0})
print(result)
