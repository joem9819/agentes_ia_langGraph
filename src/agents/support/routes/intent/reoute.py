from typing import Literal
from langchain.chat_models import init_chat_model

from pydantic import BaseModel, Field

from agents.support.state import State
from agents.support.routes.intent.prompt import SYSTEM_PROMPT


class RoutenIntent(BaseModel):
    """información de contacto de una persona"""
    step: Literal["conversation","booking"] =Field(  #el modelo tiene un campo llamado step que solo puede ser "rag_node" o "booking_node"
        "conversation", description="El siguiente paso en el proceso de enrutamiento." 
        )##ste campo es opcional (resgresa conversation por defualt) y describe cuál es el siguiente paso en el proceso de ruteo.”

llm= init_chat_model("gpt-4.1-mini", temperature=0)
llm=llm.with_structured_output(schema=RoutenIntent)



def intent_reoute(state:State)->Literal["conversation","booking"]:
    """Función para determinar el siguiente paso en el proceso de enrutamiento basado en la intención del usuario."""
    history=state["messages"]
   
    schema=llm.invoke([("system",SYSTEM_PROMPT)]+ history)
    if schema.step is not None:
        return schema.step
    return "conversation"