from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ClinicaDental:
    def __init__(self):
        self.turnos = []

    def agregar_paciente(self, nombre: str):
        self.turnos.append(nombre)

    def atender_siguiente(self):
        if not self.turnos:
            return None
        return self.turnos.pop(0)

    def agregar_urgencia(self, nombre: str):
        self.turnos.insert(0, nombre)

    def mostrar_cola(self):
        return self.turnos

    def estimar_tiempo_espera(self, minutos_por_paciente: int):
        return len(self.turnos) * minutos_por_paciente

clinica = ClinicaDental()

class Paciente(BaseModel):
    nombre: str

@app.post("/pacientes")
def agregar_paciente_endpoint(paciente: Paciente):
    clinica.agregar_paciente(paciente.nombre)
    return {"mensaje": f"Paciente {paciente.nombre} agregado"}

@app.post("/urgencias")
def agregar_urgencia_endpoint(paciente: Paciente):
    clinica.agregar_urgencia(paciente.nombre)
    return {"mensaje": f"Urgencia {paciente.nombre} agregada al frente"}

@app.post("/atender")
def atender_siguiente_endpoint():
    atendido = clinica.atender_siguiente()
    return {"atendido": atendido}

@app.get("/cola")
def mostrar_cola_endpoint():
    return {"cola": clinica.mostrar_cola()}

@app.get("/tiempo_espera")
def estimar_tiempo_espera_endpoint(minutos: int):
    tiempo = clinica.estimar_tiempo_espera(minutos)
    return {"tiempo_espera": tiempo}

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de la Clínica Dental"}