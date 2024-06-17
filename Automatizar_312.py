import streamlit as st
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
import time
from datetime import datetime, timedelta

# Función para leer el archivo JSON
def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error al leer el archivo JSON: {e}")
        return None

# Función para ejecutar las tareas automatizadas usando Selenium
def execute_tasks(tasks):
    driver = webdriver.Chrome(executable_path='/content/drive/MyDrive/tu_carpeta/chromedriver.exe')  # Cambia el path al chromedriver
    try:
        for task in tasks:
            task_type = task.get('type')
            if task_type == 'navigate':
                driver.get(task['url'])
            elif task_type == 'click':
                selector = task['selectors'][0]
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.click()
            elif task_type == 'change':
                selector = task['selectors'][0]
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.clear()
                element.send_keys(task['value'])
            elif task_type == 'setViewport':
                driver.set_window_size(task['width'], task['height'])
            else:
                st.write(f"Tipo de tarea no soportada: {task_type}")
        st.success("Tareas completadas exitosamente.")
    except Exception as e:
        st.error(f"Error al ejecutar las tareas: {e}")
    finally:
        driver.quit()

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
tasks_data = read_json('/content/drive/MyDrive/tu_carpeta/312.json')
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
