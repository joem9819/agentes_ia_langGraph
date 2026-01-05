# -*- coding: utf-8 -*-

from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
import random


llm = init_chat_model("gpt-4o-mini",temperature=1,streaming=False)

file_search_tool = {"type": "file_search", "vector_store_ids": ["vs_695bbe4a79248191806e48502f2c7bb0"]}
llm = llm.bind_tools([file_search_tool])

class State(MessagesState): ##estados o mencionaod como memoria compartida key messages automaticamente agregado
    customer_name:str
    my_age:int



def node_1(state:State)->State:
    
    new_state:State={}
    if state.get("customer_name") is None:
        new_state["customer_name"]="Carlos"
    else:
        new_state["my_age"]=random.randint(18,30)
    
    history = state["messages"]  ##accedo a la lista de mensajes en el estado
    if history == []:
        ai_message = llm.invoke([SystemMessage(content="Eres un asistente que habla y responde en español")]) ##si no hay mensajes previos, envío un mensaje de sistema y un mensaje humano vacío
    else:
        last_message = history[-1]
        ai_message = llm.invoke(last_message.text) ##envío la lista de mensajes al llm

    new_state["messages"]=[ai_message]  ##actualizo la lista de mensajes en el estado con la respuesta del llm
    return new_state


builder=StateGraph(State)
builder.add_node("node_1",node_1)

builder.add_edge(START,"node_1")
builder.add_edge("node_1",END)

agent=builder.compile()


