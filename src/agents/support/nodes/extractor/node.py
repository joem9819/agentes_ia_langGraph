from agents.support.state import State
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT
from langchain.chat_models import init_chat_model
from pydantic import BaseModel,Field



class ContactInfo(BaseModel):
    """contact information schema"""
    name: str = Field(..., description="full name of the person")
    phone_number: str = Field(..., description="phone number of the person")
    email: str = Field(..., description="email address of the person")
    age: str = Field(..., description="age of the person")
    tone: str = Field(..., description="the tone of the message, can be formal or informal")
    sentiment: str = Field(..., description="the sentiment of the message, can be positive, negative or neutral")


llm = init_chat_model("gpt-4o-mini",temperature=1,streaming=False)
llm = llm.with_structured_output(schema=ContactInfo)

def extrator(state:State)->State:
    ####Actualiza los datos del cliente en el estado
    history = state["messages"]
    customer_name=state.get("customer_name",None)
    new_state:State={}
    if customer_name is None or len(history)>20:
        schema=llm.invoke([("system", SYSTEM_PROMPT)] + history)
        new_state["customer_name"]=schema.name
        new_state["phone_number"]=schema.phone_number
        new_state["email"]=schema.email
        new_state["tone"]=schema.tone
        new_state["sentiment"]=schema.sentiment
        new_state["my_age"]=schema.age

    return new_state
