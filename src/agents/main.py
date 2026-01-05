# pip install -qU langchain "langchain[anthropic]"
import os

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()


model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),  # tu clave demo
     streaming=False,
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)


