from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re

# Configuración del WebDriver
PATH = "C:/Users/santiago.gauna/Desktop/chromedriver-win64/chromedriver.exe"
options = Options()
options.add_argument("--start-maximized")  # Para maximizar la ventana del navegador al iniciar
service = Service(PATH)

# Función para esperar a que aparezca un elemento en la página
def esperar_elemento(driver, by, valor, tiempo_espera=3):
    try:
        elemento = WebDriverWait(driver, tiempo_espera).until(
            EC.presence_of_element_located((by, valor))
        )
        return elemento
    except TimeoutException:
        print(f"Elemento {valor} no encontrado después de {tiempo_espera} segundos.")
        return None

def ejecutar_pruebas_nombre_apellido(driver, casos_de_prueba):
    resultados = []
    try:
        # Abrir la página web con el formulario
        driver.get("https://www.ucc.edu.ar/")  # Reemplaza con la URL del formulario

        for nombre_apellido in casos_de_prueba:
            try:
                # Rellenar el campo del formulario: Nombre y Apellido
                campo_nombre = esperar_elemento(driver, By.NAME, "name")
                if campo_nombre:
                    campo_nombre.clear()
                    campo_nombre.send_keys(nombre_apellido)

                    # Esperar un momento para que se aplique la validación
                    #time.sleep(1)

                    # Validar si el campo tiene la clase 'is-valid' o 'is-invalid'
                    clases = campo_nombre.get_attribute("class")
                    if "is-valid" in clases:
                        if not re.match(r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$", nombre_apellido):
                            raise AssertionError(f"Campo nombre '{nombre_apellido}' aceptado como válido, debería ser inválido.")
                        resultados.append((nombre_apellido, "EXITOSA - Aceptado como válido"))
                    elif "is-invalid" in clases:
                        if re.match(r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$", nombre_apellido):
                            raise AssertionError(f"Campo nombre '{nombre_apellido}' aceptado como inválido, debería ser válido.")
                        resultados.append((nombre_apellido, "EXITOSA - Rechazado como inválido"))
                    else:
                        raise AssertionError(f"Campo nombre '{nombre_apellido}' no tiene las clases 'is-valid' ni 'is-invalid'.")
                            
            except AssertionError as e:
                print(f"Fallo en la validación: {e}")
                resultados.append((nombre_apellido, "FALLIDA - Verificar validación"))

            except TimeoutException:
                print("Tiempo de espera excedido para encontrar el elemento.")
                resultados.append((nombre_apellido, "TIMEOUT - Elemento no encontrado"))

    except Exception as ex:
        print(f"Error al ejecutar las pruebas: {ex}")

    finally:
        # Cerrar el navegador al finalizar las pruebas
        driver.quit()

    return resultados

# Casos de prueba para el campo Nombre y Apellido
casos_de_prueba_nombre_apellido = [
    "Juan Pérez",
    "María García",
    "12345",  # Prueba con números, no debería aceptar
    "Carlos@",  # Prueba con caracteres especiales, no debería aceptar
    "Eduardo 123",  # Prueba con números y letras, no debería aceptar
    "Ana María",  # Prueba con nombres compuestos, debería aceptar
    "#",
]

try:
    driver = webdriver.Chrome(service=service, options=options)
    resultados_nombre_apellido = ejecutar_pruebas_nombre_apellido(driver, casos_de_prueba_nombre_apellido)

    # Contar tests fallidos y mostrar resultados
    tests_fallidos = [resultado for resultado in resultados_nombre_apellido if "FALLIDA" in resultado[1] or "TIMEOUT" in resultado[1]]
    print(f"\nResumen de tests fallidos ({len(tests_fallidos)} tests fallidos):")
    for index, (nombre_apellido, resultado) in enumerate(tests_fallidos, start=1):
        print(f"{index}. Prueba 'Nombre y Apellido - {nombre_apellido}': {resultado}")

    # Mostrar resultados exitosos
    print("\nResultados exitosos:")
    for resultado in resultados_nombre_apellido:
        if resultado not in tests_fallidos:
            print(f"Prueba 'Nombre y Apellido - {resultado[0]}': {resultado[1]}")

except Exception as ex:
    print(f"Error general: {ex}")

print("")
