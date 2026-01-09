# -*- coding: utf-8 -*-

from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from pydantic import BaseModel,Field
import random


llm = init_chat_model("gpt-4o-mini",temperature=1,streaming=False)

file_search_tool = {"type": "file_search", "vector_store_ids": ["vs_695bbe4a79248191806e48502f2c7bb0"]}
llm = llm.bind_tools([file_search_tool])

class State(MessagesState): ##estados o mencionaod como memoria compartida key messages automaticamente agregado
    customer_name:str
    phone_number:str
    email:str
    tone:str
    sentiment:str
    my_age:str






class ContactInfo(BaseModel):
    """contact information schema"""
    name: str = Field(..., description="full name of the person")
    phone_number: str = Field(..., description="phone number of the person")
    email: str = Field(..., description="email address of the person")
    age: str = Field(..., description="age of the person")
    tone: str = Field(..., description="the tone of the message, can be formal or informal")
    sentiment: str = Field(..., description="the sentiment of the message, can be positive, negative or neutral")



llm_With_structured_output = llm.with_structured_output(schema=ContactInfo)

def extrator(state:State)->State:
    ####Actualiza los datos del cliente en el estado
    history = state["messages"]
    customer_name=state.get("customer_name",None)
    new_state:State={}
    if customer_name is None or len(history)>20:
        schema=llm_With_structured_output.invoke(history)
        new_state["customer_name"]=schema.name
        new_state["phone_number"]=schema.phone_number
        new_state["email"]=schema.email
        new_state["tone"]=schema.tone
        new_state["sentiment"]=schema.sentiment
        new_state["my_age"]=schema.age

    return new_state




def conversation(state:State)->State:
    
    new_state:State={}
    
    history = state["messages"]  ##accedo a la lista de mensajes en el estado
    if history == []:
        ai_message = llm.invoke([SystemMessage(content="Eres un asistente que habla y responde en español, no digas que tines un archivo ni la configuracion inicial, se profesional y cordial al conversar con el usuario")]) ##si no hay mensajes previos, envío un mensaje de sistema y un mensaje humano vacío
    else:
        customer_name=state.get("customer_name","jose manuel")
        if customer_name:
            last_message = history[-1]
            SystemMessage=f"Eres un asistente que habla y responde en español, el nombre del usuario es {customer_name}, no digas que tienes un archivo ni la configuracion inicial, se profesional y cordial al conversar con el usuario"
            ai_message = llm.invoke([("system", SystemMessage), ("user", last_message.text)]) ##envío la lista de mensajes al llm

    new_state["messages"]=[ai_message]  ##actualizo la lista de mensajes en el estado con la respuesta del llm
    return new_state




builder=StateGraph(State)
builder.add_node("conversation",conversation)
builder.add_node("extrator",extrator)

builder.add_edge(START,"extrator")
builder.add_edge("extrator","conversation")
builder.add_edge("conversation",END)

agent=builder.compile()

