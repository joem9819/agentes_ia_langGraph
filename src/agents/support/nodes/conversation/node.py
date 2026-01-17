from agents.support.state import State
from langchain.chat_models import init_chat_model
from agents.support.nodes.conversation.prompt import SYSTEM_PROMPT
from agents.support.nodes.conversation.tools import tools

llm = init_chat_model("gpt-4.1-mini",temperature=1,streaming=False)
llm = llm.bind_tools(tools)


def conversation(state:State)->State:
    
    new_state:State={}
    
    history = state["messages"]  ##accedo a la lista de mensajes en el estado
    if history == []:
        ai_message = llm.invoke([("system", SYSTEM_PROMPT)]) ##si no hay mensajes previos, envío un mensaje de sistema y un mensaje humano vacío
    else:
        customer_name=state.get("customer_name","jose manuel")
        if customer_name:
            last_message = history[-1]
            
            ai_message = llm.invoke([("system", SYSTEM_PROMPT),("user", last_message.text)]) ##envío la lista de mensajes al llm
        else:
            ai_message = llm.invoke([("system", SYSTEM_PROMPT)]) ##envío la lista de mensajes al llm

    new_state["messages"]=[ai_message]  ##actualizo la lista de mensajes en el estado con la respuesta del llm ##equivalnete a state["messages"] = old_messages + [ai_message]
    ##equivalnete a state["messages"] = old_messages + [ai_message]
    return new_state



# def llm_node(state):
#     ai_message = llm.invoke(state["messages"])
#     return {
#         "messages": [ai_message]
    # }