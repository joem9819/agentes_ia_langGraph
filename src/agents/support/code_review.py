from langgraph.graph import StateGraph,START, END
from typing import  TypedDict
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage  

llm = init_chat_model("gpt-4.1-mini", temperature=1, streaming=False)

class SecurityReview(BaseModel):
    vulnerabilities: list[str]  =Field(description="Lista de vulnerabilidades de seguridad encontradas en el codigo", default=[])
    riskLevel: str = Field(description="Nivel de riesgo general de las vulnerabilidades", default=None)
    suggestions: list[str] = Field(description="Lista de sugerencias para corregir las vulnerabilidades", default=[])


class MaintainabilityReview(BaseModel):
    concerns: list[str] = Field(description="Lista de problemas de mantenimiento encontrados en el código", default=[])   
    qualityScore: int = Field(description="Puntaje general de calidad del código del 1 al 10", default=None, ge=1, le=10)
    recommendations: list[str] = Field(description="Lista de recomendaciones para mejorar la mantenibilidad", default=[])

class PerformanceReview(BaseModel):
    bottlenecks: list[str] = Field(description="Lista de cuellos de botella de rendimiento encontrados en el código", default=[])   
    performanceScore: int = Field(description="Puntaje general de rendimiento del código del 1 al 10", default=None, ge=1, le=10)
    optimizationSuggestions: list[str] = Field(description="Lista de sugerencias para optimizar el rendimiento", default=[])
    

class State(TypedDict):
    code: str
    security_review: SecurityReview
    maintainability_review: MaintainabilityReview
    performance_review: PerformanceReview
    final_review: str

def security_review(state: State):
    code = state["code"]
    messages = [
        ("system", "Eres experto en seguridad de código. Te centras en identificar vulnerabilidades de seguridad, riesgos de inyección y problemas de autenticación."),
        ("user", f"Revisar este código: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(SecurityReview)
    security_review = llm_with_structured_output.invoke(messages)
   
    return {
        'security_review': security_review
        }

def maintainability_review(state: State):   
    code = state['code']
    messages = [
        ("system", "Eres experto en calidad de código. Te centras en la estructura del código, legibilidad y cumplimiento con las mejores prácticas."),
        ("user", f"Revisar este código: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(MaintainabilityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {
        'maintainability_review': schema
    }

def performance_review(state: State):
    code = state['code']
    messages = [
        ("system", "Eres un experto en optimización de rendimiento de código. Te centras en identificar cuellos de botella, uso ineficiente de recursos y problemas de escalabilidad."),
        ("user", f"Revisar este código: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(PerformanceReview)
    performance_review = llm_with_structured_output.invoke(messages)
    return {
        'performance_review': performance_review
    }

def aggregator(state: State):
    security_review = state['security_review']
    maintainability_review = state['maintainability_review']
    performance_review = state['performance_review']
    messages = [
        ("system", "Eres un líder técnico que resume múltiples revisiones de código"),
        ("user", f"Sintetice estos resultados de revisión de código en un resumen conciso con acciones clave: Revisión de seguridad: {security_review} y mantenibilidad: {maintainability_review} y rendimiento: {performance_review}")
    ]
    response = llm.invoke(messages)
    return {
        'final_review': response.text
    }



builder=StateGraph(State)

builder.add_node("security_review", security_review)    
builder.add_node("maintainability_review", maintainability_review)
builder.add_node("performance_review", performance_review)
builder.add_node("aggregator", aggregator)

builder.add_edge(START, "security_review")
builder.add_edge(START, "maintainability_review")
builder.add_edge(START, "performance_review")
builder.add_edge("security_review", "aggregator")
builder.add_edge("maintainability_review", "aggregator")
builder.add_edge("performance_review", "aggregator")
builder.add_edge("aggregator", END)  
agent = builder.compile()