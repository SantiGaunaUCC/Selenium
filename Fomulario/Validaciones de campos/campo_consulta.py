from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


# Configuración del WebDriver
PATH = "C:/Users/santiago.gauna/Desktop/chromedriver-win64/chromedriver.exe"
options = Options()
options.add_argument("--start-maximized")  # Para maximizar la ventana del navegador al iniciar
service = Service(PATH)

# Función para esperar a que aparezca un elemento en la página
def esperar_elemento(driver, by, valor, tiempo_espera=5):
    try:
        elemento = WebDriverWait(driver, tiempo_espera).until(
            EC.presence_of_element_located((by, valor))
        )
        return elemento
    except TimeoutException:
        print(f"Elemento {valor} no encontrado después de {tiempo_espera} segundos.")
        return None
    

def ejecutar_pruebas_consulta(driver, casos_de_prueba):
    resultados = []
    try:
        driver.get("https://www.ucc.edu.ar/")
        
        for consulta in casos_de_prueba:
            try:
                campo_consulta = esperar_elemento(driver, By.NAME, "Escribí tu consulta")
                if campo_consulta:
                    campo_consulta.clear()
                    campo_consulta.send_keys(consulta)
                    
                    # Esperar un momento para que se aplique la validación
                    #time.sleep(1)

                    # Verificar si el campo tiene la clase 'is-valid' y cumple con la longitud mínima
                    clases = campo_consulta.get_attribute("class")
                    if "is-valid" in clases:
                        if len(consulta) >= 3:
                            resultados.append((consulta, "EXITOSA - Aceptado como válido"))
                    elif "is-invalid" in clases:
                        if not len(consulta) >= 3:
                            resultados.append((consulta, "EXITOSA - Rechazado como inválido"))
                    else:
                        resultados.append((consulta, "FALLIDA - No se encontró clase 'is-valid' o 'is-invalid'"))

            except TimeoutException:
                resultados.append((consulta, "TIMEOUT - Elemento no encontrado"))

    except Exception as ex:
        print(f"Error al ejecutar las pruebas de Consulta: {ex}")

    finally:
        # Cerrar el navegador al finalizar las pruebas
        driver.quit()

    return resultados


# Casos de prueba para el campo de Consulta
casos_de_prueba_consulta = [
    "Estoy interesado en la carrera de Ingeniería Informática.",
    "Me gustaría obtener más información sobre el programa de Biología.",
    "Quiero inscribirme en la Maestría en Administración de Empresas.",
    "12345",  # Prueba con números, debería aceptar
    "q",  # Prueba con texto demasiado corto, no debería aceptar
    "qq"  # Prueba con texto demasiado corto, no debería aceptar
]

try:
    driver = webdriver.Chrome(service=service, options=options)
    resultados_consulta = ejecutar_pruebas_consulta(driver, casos_de_prueba_consulta)

    # Contar tests fallidos y mostrar resultados
    tests_fallidos = [resultado for resultado in resultados_consulta if "FALLIDA" in resultado[1] or "TIMEOUT" in resultado[1]]
    print(f"\nResumen de tests fallidos ({len(tests_fallidos)} tests fallidos):")
    for index, (consulta, resultado) in enumerate(tests_fallidos, start=1):
        print(f"{index}. Prueba 'Consulta - {consulta}': {resultado}")

    # Mostrar resultados exitosos
    print("\nResultados exitosos:")
    for resultado in resultados_consulta:
        if resultado not in tests_fallidos:
            print(f"Prueba 'Consulta - {resultado[0]}': {resultado[1]}")

except Exception as ex:
    print(f"Error general: {ex}")