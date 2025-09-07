from typing import List, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from Chain import generation_chain, reflection_chain

load_dotenv()

REFLECT = "reflect"
GENERATE = "generate"
graph = MessageGraph()

def generateNode(state):
    return generation_chain.invoke({
        'messages':state
    })

def ReFlectionNode(state):
    response=reflection_chain.invoke({
        'messages':state
    })    
    return [HumanMessage(content=response.content)]

def ShouldContinue(state):
    if(len(state)>3):
        return END
    return REFLECT

graph.add_node(GENERATE,generateNode)
graph.add_node(REFLECT,ReFlectionNode)
graph.add_conditional_edges(GENERATE,ShouldContinue)
graph.set_entry_point(GENERATE)
graph.add_edge(REFLECT,GENERATE)
app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()
response = app.invoke(HumanMessage(content="How Has Hania Amir Gotten Famous?"))

print(response)
