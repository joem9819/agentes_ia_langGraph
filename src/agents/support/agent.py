from langgraph.graph import StateGraph, START, END, MessagesState

from agents.support.state import State
from agents.support.nodes.extractor.node import extrator
from agents.support.nodes.conversation.node import conversation

builder=StateGraph(State)
builder.add_node("conversation",conversation)
builder.add_node("extrator",extrator)

builder.add_edge(START,"extrator")
builder.add_edge("extrator","conversation")
builder.add_edge("conversation",END)

agent=builder.compile()


