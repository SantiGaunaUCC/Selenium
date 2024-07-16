from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re

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

def ejecutar_pruebas_email(driver, casos_de_prueba):
    resultados = []
    try:
        # Abrir la página web con el formulario
        driver.get("https://www.ucc.edu.ar/")  # Reemplaza con la URL del formulario

        for email in casos_de_prueba:
            try:
                # Rellenar el campo del formulario: Email
                campo_email = esperar_elemento(driver, By.NAME, "email")
                if campo_email:
                    campo_email.clear()
                    campo_email.send_keys(email)

                    # Esperar un momento para que se aplique la validación
                    # time.sleep(1)

                    # Validar si el campo tiene la clase 'is-valid' o 'is-invalid'
                    clases = campo_email.get_attribute("class")
                    if "is-valid" in clases:
                        if not re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email):
                            raise AssertionError(f"Campo email '{email}' aceptado como válido, debería ser inválido.")
                        resultados.append((email, "EXITOSA - Aceptado como válido"))
                    elif "is-invalid" in clases:
                        if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email):
                            raise AssertionError(f"Campo email '{email}' aceptado como inválido, debería ser válido.")
                        resultados.append((email, "EXITOSA - Rechazado como inválido"))
                    else:
                        raise AssertionError(f"Campo email '{email}' no tiene las clases 'is-valid' ni 'is-invalid'.")
                            
            except AssertionError as e:
                print(f"Fallo en la validación: {e}")
                resultados.append((email, "FALLIDA - Verificar validación"))

            except TimeoutException:
                print("Tiempo de espera excedido para encontrar el elemento.")
                resultados.append((email, "TIMEOUT - Elemento no encontrado"))

    except Exception as ex:
        print(f"Error al ejecutar las pruebas de Email: {ex}")

    finally:
        # Cerrar el navegador al finalizar las pruebas
        driver.quit()

    return resultados

# Casos de prueba para el campo Email
casos_de_prueba_email = [
    "correo@example.com",
    "correo@dominio", # No debería ser válido
    "usuario@dominio.com.ar",
    "correo sin arroba",  # Prueba con formato incorrecto, no debería aceptar
]

try:
    driver = webdriver.Chrome(service=service, options=options)
    resultados_email = ejecutar_pruebas_email(driver, casos_de_prueba_email)

    # Contar tests fallidos y mostrar resultados
    tests_fallidos = [resultado for resultado in resultados_email if "FALLIDA" in resultado[1] or "TIMEOUT" in resultado[1]]
    print(f"\nResumen de tests fallidos ({len(tests_fallidos)} tests fallidos):")
    for index, (email, resultado) in enumerate(tests_fallidos, start=1):
        print(f"{index}. Prueba 'Email - {email}': {resultado}")

    # Mostrar resultados exitosos
    print("\nResultados exitosos:")
    for resultado in resultados_email:
        if resultado not in tests_fallidos:
            print(f"Prueba 'Email - {resultado[0]}': {resultado[1]}")

except Exception as ex:
    print(f"Error general: {ex}")
