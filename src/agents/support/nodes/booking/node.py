# pip install -qU langchain "langchain[anthropic]"
import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from agents.support.nodes.booking.tools import tools
from agents.support.nodes.booking.prompt import prompt_template


from dotenv import load_dotenv
load_dotenv()



booking_node= create_agent(
    model="gpt-4.1-mini",
    tools=tools,
    system_prompt=prompt_template.format(),
)
