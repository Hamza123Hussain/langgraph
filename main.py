from typing import Dict,TypedDict
from langgraph.graph import StateGraph
class AgentState(TypedDict):
    message:str

def greetingnode(state:AgentState)-> AgentState:
    state['message']  = 'Hey ' + state['message'] + ', how are you doing '
    
    return state   

graph=StateGraph(AgentState)
graph.add_node('greeter',greetingnode)
graph.set_entry_point('greeter')
graph.set_finish_point('greeter')
app=graph.compile()

