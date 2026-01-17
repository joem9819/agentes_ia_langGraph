from langchain_core.tools import tool

@tool("book_appointment", description="Reservar una cita médica para una fecha, hora, médico y paciente determinados.")
def book_appointment(date: str, time: str, doctor: str, patient: str) -> str:
    ## TODO: Implement the booking logic
    return f"Appointment booked for {date} at {time} with {doctor} for {patient}!"

@tool("get_appointment_availability", description="Obtener la disponibilidad de una cita médica para una fecha, hora y médico determinados.")
def get_appointment_availability(date: str, time: str, doctor: str) -> str:
    ## TODO: Implement the availability logic
    return f"""
    The availability slots for the {doctor} are:
    - Monday: 10:00-15:00
    - Wednesday: 10:00-15:00
    - Thursday: 10:00-15:00
    - Friday: 10:00-12:00
    """


tools = [book_appointment, get_appointment_availability]