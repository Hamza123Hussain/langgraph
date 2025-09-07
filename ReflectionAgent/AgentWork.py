from typing import List, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from Chain import generation_chain, reflection_chain  # 👈 importing from Code 1

load_dotenv()

# ---------------------------------------------------
# Define constants for node names
# ---------------------------------------------------
REFLECT = "reflect"
GENERATE = "generate"

# ---------------------------------------------------
# Create a MessageGraph (works directly with messages instead of dict state)
# ---------------------------------------------------
graph = MessageGraph()

# ---------------------------------------------------
# Node 1: "Generate" node
# This calls the generation_chain and produces a tweet
# ---------------------------------------------------
def generateNode(state):
    # state here is the conversation history (list of messages)
    return generation_chain.invoke({
        'messages': state   # 👈 pass the full chat history into the chain
    })

# ---------------------------------------------------
# Node 2: "Reflection" node
# This critiques the previous tweet and returns feedback
# ---------------------------------------------------
def ReFlectionNode(state):
    # Call reflection chain with the entire conversation history
    response = reflection_chain.invoke({
        'messages': state
    })    
    # Return critique as a HumanMessage (so it's treated like user feedback in history)
    return [HumanMessage(content=response.content)]

# ---------------------------------------------------
# Conditional function: should we continue or stop?
# ---------------------------------------------------
def ShouldContinue(state):
    # If there are more than 3 messages in history, stop looping
    if(len(state) > 3):
        return END
    # Otherwise, go to reflection node
    return REFLECT

# ---------------------------------------------------
# Add nodes to the graph
# ---------------------------------------------------
graph.add_node(GENERATE, generateNode)
graph.add_node(REFLECT, ReFlectionNode)

# ---------------------------------------------------
# Add conditional edge:
# After "generate" → check ShouldContinue()
#   - If END → finish
#   - Else → go to REFLECT
# ---------------------------------------------------
graph.add_conditional_edges(GENERATE, ShouldContinue)

# ---------------------------------------------------
# Entry point = GENERATE node
# After reflection → go back to generate
# ---------------------------------------------------
graph.set_entry_point(GENERATE)
graph.add_edge(REFLECT, GENERATE)

# ---------------------------------------------------
# Compile the graph into an app
# ---------------------------------------------------
app = graph.compile()

# ---------------------------------------------------
# Debugging visualization of graph
# ---------------------------------------------------
print(app.get_graph().draw_mermaid())  # Mermaid syntax diagram
app.get_graph().print_ascii()          # ASCII diagram

# ---------------------------------------------------
# Run the app with initial human input
# ---------------------------------------------------
response = app.invoke(HumanMessage(content="How Has Hania Amir Gotten Famous?"))

print(response)   # 👈 Final output after looping
