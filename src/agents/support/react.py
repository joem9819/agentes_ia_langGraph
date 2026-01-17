# pip install -qU langchain "langchain[anthropic]"
import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent



from langchain_core.tools import tool
import requests

@tool("get_products", description="Obtén los productos que ofrece la tienda filtrando por precio")
def get_products():
    # Connnect with API
    """Consigue los productos que ofrece la tienda"""
    response = requests.get("https://api.escuelajs.co/api/v1/products")
    products = response.json()
    return "".join([f"{product['title']} - {product['price']}" for product in products])


@tool("get_weather", description="Get the weather of a city")
def get_weather(city: str):
    response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1")
    data = response.json()
    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
    data = response.json()
    response = f"The weather in {city} is {data["current_weather"]["temperature"]}C with {data["current_weather"]["windspeed"]}km/h of wind."
    return response


tools = [get_products, get_weather]


from dotenv import load_dotenv
load_dotenv()


system_prompt = """
Eres un asistente de ventas que ayuda a los clientes a encontrar los productos que necesitan y dar el clima de la ciudad

Tus tools son:
- get_products: para obtener los productos que ofreces en la tienda
- get_weather: para obtener el clima de la ciudad
"""


agent= create_agent(
    model="gpt-4.1-mini",
    tools=tools,
    system_prompt=system_prompt,
)
