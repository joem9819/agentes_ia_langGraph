from agents.support.routes.intent.reoute import intent_reoute
from langgraph.graph import StateGraph, START, END, MessagesState

from agents.support.state import State
from agents.support.nodes.extractor.node import extrator
from agents.support.nodes.conversation.node import conversation
from agents.support.nodes.booking.node import booking_node


builder=StateGraph(State)
builder.add_node("conversation",conversation)
builder.add_node("extrator",extrator)
builder.add_node("booking",booking_node)

builder.add_edge(START,"extrator")
builder.add_conditional_edges("extrator",intent_reoute)
builder.add_edge("booking",END)
builder.add_edge("conversation",END)

agent=builder.compile()


