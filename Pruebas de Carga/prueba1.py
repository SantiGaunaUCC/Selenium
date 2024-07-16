from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import concurrent.futures
import time

# Configuración del WebDriver
PATH = "C:/Users/santiago.gauna/Desktop/chromedriver-win64/chromedriver.exe"
options = Options()
options.add_argument("--start-maximized")
service = Service(PATH)

# Función para esperar a que aparezca un elemento en la página
def esperar_elemento(driver, by, valor, tiempo_espera=10):
    try:
        elemento = WebDriverWait(driver, tiempo_espera).until(
            EC.presence_of_element_located((by, valor))
        )
        return elemento
    except TimeoutException:
        print(f"Elemento {valor} no encontrado después de {tiempo_espera} segundos.")
        return None

# Función para simular una consulta y validar el campo
def simular_consulta(usuario, consulta):
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.ucc.edu.ar/")  # Reemplaza con la URL de tu página

        # Encontrar el campo de consulta y enviar la consulta
        campo_consulta = esperar_elemento(driver, By.NAME, "Escribí tu consulta")
        if campo_consulta:
            campo_consulta.clear()
            campo_consulta.send_keys(consulta)
            time.sleep(1)  # Esperar para que se aplique la validación

            # Verificar si el campo tiene la clase 'is-valid' o 'is-invalid'
            clases = campo_consulta.get_attribute("class")
            if "is-valid" in clases:
                print(f"Usuario {usuario}: Consulta '{consulta}' válida.")
            elif "is-invalid" in clases:
                print(f"Usuario {usuario}: Consulta '{consulta}' inválida.")
            else:
                print(f"Usuario {usuario}: Estado desconocido para consulta '{consulta}'.")

    except Exception as ex:
        print(f"Error en el usuario {usuario}: {ex}")

    finally:
        if driver:
            driver.quit()

# Lista de consultas de prueba
consultas = [
    "Estoy interesado en la carrera de Ingeniería Informática.",
    "Me gustaría obtener más información sobre el programa de Biología.",
    "Quiero inscribirme en la Maestría en Administración de Empresas.",
    "12345",  # Prueba con números, debería aceptar
    "q",  # Prueba con texto demasiado corto, no debería aceptar
    "qq"  # Prueba con texto demasiado corto, no debería aceptar
]

# Simular múltiples usuarios enviando consultas simultáneamente
num_usuarios = len(consultas)
with concurrent.futures.ThreadPoolExecutor() as executor:
    for usuario, consulta in enumerate(consultas, start=1):
        executor.submit(simular_consulta, usuario, consulta)

print(f"Simulación de carga completada para {num_usuarios} usuarios.")


