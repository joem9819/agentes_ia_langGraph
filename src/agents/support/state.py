
from langgraph.graph import StateGraph, START, END, MessagesState

class State(MessagesState): ##estados o mencionaod como memoria compartida key messages automaticamente agregado
    customer_name:str
    phone_number:str
    email:str
    tone:str
    sentiment:str
    my_age:str
