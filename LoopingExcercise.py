# ===========================================
# LangGraph Guessing Game (Manual Input)
# ===========================================

# --- Imports ---
from langgraph.graph import StateGraph, END   # Core LangGraph classes
from typing import List, TypedDict            # Type hints for better clarity

# --- Game Configuration ---
guess = 14  # 🎯 Target number the player needs to guess

# ===========================================
# 1. Defining the Agent's State
# ===========================================
# In LangGraph, we keep all the data in a "state" object (a Python dictionary).
# TypedDict is used to specify exactly what keys our state will have
# so Python can check for errors before we even run the code.
class AgentState(TypedDict):
    name: str           # Player's name (string)
    guesses: List[int]  # List of all guesses so far (list of integers)
    counter: int        # Number of guesses attempted (integer)

# ===========================================
# 2. First Node: Greeting Node
# ===========================================
# Runs at the very start — welcomes the player and resets the guess counter.
def greeting_node(state: AgentState) -> AgentState:
    # Add a friendly greeting message to the "name" field
    state["name"] = f"Hi there, {state['name']}"

    # Reset guess counter to 0 before starting the game
    state["counter"] = 0

    # Must always return the updated state
    return state

# ===========================================
# 3. Second Node: Input Node
# ===========================================
# This node asks the player to manually enter a guess via the terminal.
def input_node(state: AgentState) -> AgentState:
    # Prompt user for a number — `input()` pauses the program until user types something
    user_number = int(input("Enter your guess: "))

    # Store the guess in the state's "guesses" list
    state["guesses"].append(user_number)

    # Increment the counter to track how many guesses have been made
    state["counter"] += 1

    return state

# ===========================================
# 4. Decision Function: Should Continue?
# ===========================================
# This function decides where to go next in the graph:
#   - If guess is correct → go to "exit"
#   - If too high / too low → loop back to "input"
#   - If out of attempts → exit
def should_continue(state: AgentState) -> str:
    # Get the latest guess (last element in the guesses list)
    latest_guess = state['guesses'][-1]

    # Case 1: Correct guess
    if latest_guess == guess:
        print("🎉 Correct guess!")
        return "exit"  # This matches the key in our routing map below

    # Case 2: Ran out of attempts
    elif state["counter"] >= 7:
        print("❌ Out of attempts!")
        return "exit"

    # Case 3: Too high
    elif latest_guess > guess:
        print("Too high!")
        return "loop"

    # Case 4: Too low
    else:
        print("Too low!")
        return "loop"

# ===========================================
# 5. Building the Graph
# ===========================================
# Create a new graph with our defined state shape (AgentState)
graph = StateGraph(AgentState)

# Add each "node" — these are like functions in the pipeline
graph.add_node("greeting", greeting_node)  # Start node
graph.add_node("input", input_node)        # Player input node

# Connect greeting → input (first step)
graph.add_edge("greeting", "input")

# Add conditional routing:
# After "input" runs, the should_continue() function decides next step.
graph.add_conditional_edges(
    "input",           # The node we are branching from
    should_continue,   # Function that returns either "loop" or "exit"
    {
        "loop": "input",  # If "loop", go back to input node
        "exit": END       # If "exit", stop the graph
    }
)

# Set starting node
graph.set_entry_point("greeting")

# ===========================================
# 6. Compile the Graph
# ===========================================
# This converts our node/edge definitions into an actual runnable app.
app = graph.compile()

# ===========================================
# 7. Run the Game
# ===========================================
# Pass the starting state to app.invoke()
#   - name → "Player"
#   - guesses → empty list (no guesses yet)
#   - counter → 0 (no attempts yet)
app.invoke({"name": "Player", "guesses": [], "counter": 0})
