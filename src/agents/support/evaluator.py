from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

class State(TypedDict):
    joke: str
    topic: str
    feedback: str
    is_funny: str
    intent:int

class Feedback(BaseModel):
    is_funny: bool = Field(
        description="Decide si el chiste es gracioso o no. Devuelve Verdadero si lo es, Falso en caso contrario."
    )
    feedback: str = Field(
        description="Si el chiste no es gracioso, proporciona comentarios sobre cómo mejorarlo.",
    )

llm = init_chat_model("openai:gpt-4.1-mini", temperature=0)
ll_evaluator = llm.with_structured_output(Feedback, temperature=0)


SYSTEM_PROMPT = """
Un chiste graciso debe ser mas de 2 parrafo.
"""


def generator_node(state: State):
    feedback = state.get("feedback", None)
    topic = state.get("topic", None)
    if feedback:
        msg = llm.invoke(f"Crea un chiste sobre {topic} considerando el siguiente comentario: {feedback} Responde en español")
    else:
        msg = llm.invoke(f"Crea un chiste sobre {topic} y responde en español")
    return {"joke": msg.text}


def evaluator_node(state: State):
    joke = state.get("joke", None)
    schema = ll_evaluator.invoke(f"Grade the joke {joke} with the following prompt: {SYSTEM_PROMPT}")
    return {"is_funny": schema.is_funny, "feedback": schema.feedback}


def route_edge(state: State) -> Literal[END, "generator_node"]:
    is_funny = state.get("is_funny", True)
    intent=state.get("intent",0)
    if is_funny:
        return END
    else:
        if intent>=2:
            print("Maximo numero de intentos alcanzado")
            return END
        else:
            state["intent"]=intent+1
        return "generator_node"


builder = StateGraph(State)

builder.add_node('generator_node', generator_node)
builder.add_node('evaluator_node', evaluator_node)

builder.add_edge(START, 'generator_node')
builder.add_edge('generator_node', 'evaluator_node')
builder.add_conditional_edges('evaluator_node', route_edge)
agent = builder.compile()