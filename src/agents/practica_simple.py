from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    customer_name: str
    my_age: int
    is_verified: bool
    discount_applied: float
    final_message: str

def validate_customer(state: State):
    """Nodo 1: Valida los datos del cliente"""
    print(f"[Validate] Procesando cliente: {state.get('customer_name', 'Sin nombre')}")

    # Si no hay nombre, asignar uno por defecto
    if state.get("customer_name") is None:
        return {
            "customer_name": "joselo",
            "is_verified": False
        }

    # Si hay nombre, el cliente está verificado
    return {
        "is_verified": True
    }

def calculate_discount(state: State):
    """Nodo 2: Calcula descuento basado en la edad"""
    print(f"[Calculate] Cliente verificado: {state.get('is_verified')}")

    age = state.get("my_age", 0)
    discount = 0.0

    # Lógica de descuentos por edad
    if age < 18:
        discount = 0.05  # 5% para menores
    elif age >= 18 and age < 65:
        discount = 0.10  # 10% para adultos
    else:
        discount = 0.20  # 20% para adultos mayores

    print(f"[Calculate] Edad: {age}, Descuento: {discount * 100}%")

    return {
        "discount_applied": discount
    }

def generate_summary(state: State):
    """Nodo 3: Genera un mensaje final con el resumen"""
    name = state.get("customer_name", "Desconocido")
    age = state.get("my_age", 0)
    verified = state.get("is_verified", False)
    discount = state.get("discount_applied", 0.0)

    message = f"""
    === RESUMEN DEL CLIENTE ===
    Nombre: {name}
    Edad: {age} años
    Verificado: {'Sí' if verified else 'No'}
    Descuento aplicado: {discount * 100}%
    ===========================
    """

    print(message)

    return {
        "final_message": message.strip()
    }

# Construir el grafo
builder = StateGraph(State)

# Agregar los nodos
builder.add_node("validate_customer", validate_customer)
builder.add_node("calculate_discount", calculate_discount)
builder.add_node("generate_summary", generate_summary)

# Definir el flujo secuencial
builder.add_edge(START, "validate_customer")
builder.add_edge("validate_customer", "calculate_discount")
builder.add_edge("calculate_discount", "generate_summary")
builder.add_edge("generate_summary", END)

# Compilar el agente
agent = builder.compile()
