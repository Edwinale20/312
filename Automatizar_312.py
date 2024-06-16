import streamlit as st
import json
import time
from datetime import datetime, timedelta
from threading import Thread

# Función para leer el archivo JSON
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Función para ejecutar las tareas automatizadas (simulada)
def execute_tasks(tasks):
    for task in tasks:
        st.write(f"Ejecutando tarea: {task['type']}")

# Función para calcular el tiempo restante hasta la siguiente ejecución
def time_until_next_execution(hour, minute):
    now = datetime.now()
    next_execution = datetime(now.year, now.month, now.day, hour, minute)
    if now >= next_execution:
        next_execution += timedelta(days=1)
    return (next_execution - now).total_seconds()

# Función para ejecutar tareas diariamente a una hora específica
def schedule_daily_tasks(tasks, hour, minute):
    while True:
        wait_time = time_until_next_execution(hour, minute)
        st.write(f"Esperando {wait_time} segundos hasta la próxima ejecución.")
        time.sleep(wait_time)
        execute_tasks(tasks)

# Streamlit UI
st.title('Automatización de Tareas con Streamlit')

# Leer el archivo JSON con las tareas automatizadas
tasks = read_json('312.json')
st.write("Tareas cargadas exitosamente.")

if st.button('Iniciar Automatización'):
    st.write('Las tareas se ejecutarán todos los días a las 4:40 PM.')
    # Ejecutar en un nuevo hilo para no bloquear la interfaz de usuario de Streamlit
    t = Thread(target=schedule_daily_tasks, args=(tasks, 16, 46))
    t.start()
