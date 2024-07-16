from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time

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

def ejecutar_pruebas_seleccion(driver, casos_de_prueba):
    resultados = []
    try:
        # Abrir la página web con el formulario
        driver.get("https://www.ucc.edu.ar/")  # Reemplaza con la URL del formulario

        for opcion_texto in casos_de_prueba:
            try:
                # Seleccionar una opción del campo de selección
                campo_seleccion = esperar_elemento(driver, By.ID, "validationCustom0")
                if campo_seleccion:
                    select = Select(campo_seleccion)
                    select.select_by_visible_text(opcion_texto)

                    # Esperar un momento para que se aplique la validación
                    #time.sleep(1)

                    # Verificar si la opción seleccionada es la esperada
                    selected_option = select.first_selected_option.text
                    if selected_option == opcion_texto:
                        # Verificar si el campo tiene la clase 'is-valid'
                        clases = campo_seleccion.get_attribute("class")
                        if "is-valid" in clases:
                            resultados.append((opcion_texto, "EXITOSA"))
                        else:
                            resultados.append((opcion_texto, "FALLIDA - No tiene clase 'is-valid'"))
                    else:
                        resultados.append((opcion_texto, f"FALLIDA - Opción seleccionada: '{selected_option}'"))

            except TimeoutException:
                resultados.append((opcion_texto, "TIMEOUT"))

    except Exception as ex:
        print(f"Error al ejecutar las pruebas de Selección: {ex}")

    finally:
        # Cerrar el navegador al finalizar las pruebas
        driver.quit()

    return resultados

# Casos de prueba para el campo de selección
casos_de_prueba_seleccion = [
    "Jornadas de Puertas Abiertas",
    "Carreras de grado",
    "Carreras de pregrado",
    "Carreras de articulación",
    "Carreras de posgrado",
    "Cursos de posgrado",
    "Diplomados y diplomaturas",
    "Especializaciones",
    "Cursos",
    "Profesorados",
    "Otra"
]

try:
    driver = webdriver.Chrome(service=service, options=options)
    resultados_seleccion = ejecutar_pruebas_seleccion(driver, casos_de_prueba_seleccion)
    
    # Contar tests fallidos y mostrar resultados
    tests_fallidos = [resultado for resultado in resultados_seleccion if "FALLIDA" in resultado[1] or "TIMEOUT" in resultado[1]]
    print(f"\nResumen de tests fallidos ({len(tests_fallidos)} tests fallidos):")
    for index, (opcion_texto, resultado) in enumerate(tests_fallidos, start=1):
        print(f"{index}. Prueba 'Categoría - {opcion_texto}': {resultado}")

    # Mostrar resultados exitosos
    print("\nResultados exitosos:")
    for resultado in resultados_seleccion:
        if resultado not in tests_fallidos:
            print(f"Prueba 'Categoría - {resultado[0]}': {resultado[1]}")

except Exception as ex:
    print(f"Error general: {ex}")

print("")
