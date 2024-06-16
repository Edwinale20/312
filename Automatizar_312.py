import streamlit as st
import json
import time
from datetime import datetime, timedelta
from threading import Thread

# Función para leer el archivo JSON
def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error al leer el archivo JSON: {e}")
        return None

# Función para ejecutar las tareas automatizadas (simulada)
def execute_tasks(tasks):
    if tasks:
        for task in tasks:
            if isinstance(task, dict):
                task_type = task.get('type')
                if task_type:
                    st.write(f"Ejecutando tarea: {task_type}")
                else:
                    st.write("Error: Tarea no tiene el atributo 'type'")
            else:
                st.write("Error: Formato de tarea inválido. Cada tarea debe ser un diccionario.")
    else:
        st.error("No se pudieron ejecutar las tareas porque el archivo JSON no se cargó correctamente.")

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
tasks_data = read_json('312.json')
tasks = tasks_data.get('steps') if tasks_data else None

if tasks:
    st.write("Tareas cargadas exitosamente.")
else:
    st.error("No se pudieron cargar las tareas del archivo JSON.")

if st.button('Iniciar Automatización'):
    if tasks:
        st.write('Las tareas se ejecutarán todos los días a las 4:40 PM.')
        # Ejecutar en un nuevo hilo para no bloquear la interfaz de usuario de Streamlit
        t = Thread(target=schedule_daily_tasks, args=(tasks, 16, 40))
        t.start()
    else:
        st.error("No se pueden iniciar las tareas automáticas porque no se cargaron correctamente.")

if st.button('Ejecutar Tareas Manualmente'):
    if tasks:
        st.write('Ejecutando tareas manualmente.')
        execute_tasks(tasks)
    else:
        st.error("No se pueden ejecutar las tareas manualmente porque no se cargaron correctamente.")
