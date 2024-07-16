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
def esperar_elemento(driver, by, valor, tiempo_espera=10):
    try:
        elemento = WebDriverWait(driver, tiempo_espera).until(
            EC.presence_of_element_located((by, valor))
        )
        return elemento
    except TimeoutException:
        print(f"Elemento {valor} no encontrado después de {tiempo_espera} segundos.")
        return None

def ejecutar_pruebas_celular(driver, casos_de_prueba):
    resultados = []
    try:
        # Abrir la página web con el formulario
        driver.get("https://www.ucc.edu.ar/")  # Reemplaza con la URL del formulario

        for celular in casos_de_prueba:
            try:
                # Seleccionar el código de país (+54)
                select_pais = esperar_elemento(driver, By.CLASS_NAME, "PhoneInputInput")
                if select_pais:
                    # Verificar el valor del código de país actual
                    valor_codigo_pais = select_pais.get_attribute("value")
                
                # Rellenar el campo del formulario: Celular
                campo_celular = esperar_elemento(driver, By.NAME, "phone")
                if campo_celular:
                    # Concatenar el número de celular con el código de país actual
                    nuevo_valor_celular = f"{valor_codigo_pais} {celular}"

                    # Ingresar el nuevo número de celular junto con el código de país
                    campo_celular.clear()
                    campo_celular.send_keys(nuevo_valor_celular)

                    # Esperar un momento para que se aplique la validación
                    #time.sleep(1)

                    # Verificar si el campo tiene la clase 'is-valid' o 'is-invalid'
                    clases = campo_celular.get_attribute("class")
                    if "is-valid" in clases:
                        if celular.isdigit() and len(celular) == 10:
                            resultados.append((nuevo_valor_celular, "EXITOSA - Aceptado como válido"))
                        else:
                            raise AssertionError(f"Campo celular '{nuevo_valor_celular}' aceptado como válido, debería ser inválido.")
                            
                    elif "is-invalid" in clases:
                        if not celular.isdigit() or len(celular) != 10:
                            resultados.append((nuevo_valor_celular, "EXITOSA - Rechazado como inválido"))
                        else:
                            raise AssertionError(f"Campo celular '{nuevo_valor_celular}' aceptado como inválido, debería ser válido.")
                            
                    else:
                        raise AssertionError(f"Campo celular '{nuevo_valor_celular}' no tiene las clases 'is-valid' ni 'is-invalid'.")
                            
            except AssertionError as e:
                print(f"Fallo en la validación: {e}")
                resultados.append((nuevo_valor_celular, "FALLIDA - Verificar validación"))

            except TimeoutException:
                print("Tiempo de espera excedido para encontrar el elemento.")
                resultados.append((nuevo_valor_celular, "TIMEOUT - Elemento no encontrado"))

    except Exception as ex:
        print(f"Error al ejecutar las pruebas de Celular: {ex}")

    finally:
        # Cerrar el navegador al finalizar las pruebas
        driver.quit()

    return resultados

# Casos de prueba para el campo Celular
casos_de_prueba_celular = [
    "3512345678",
    "1234567890",
    "12345",  # Prueba con longitud incorrecta, no debería aceptar
    "abcdefghij",  # Prueba con caracteres no numéricos, no debería aceptar
    "+543512345678",  # Prueba con formato internacional
    "123-456-7890",  # Prueba con formato separado
    "123456789012345",  # Prueba con número de teléfono demasiado largo
    "1",  # Prueba con número de teléfono muy corto
    "",  # Prueba con campo vacío
]

try:
    driver = webdriver.Chrome(service=service, options=options)
    resultados_celular = ejecutar_pruebas_celular(driver, casos_de_prueba_celular)

    # Contar tests fallidos y mostrar resultados
    tests_fallidos = [resultado for resultado in resultados_celular if "FALLIDA" in resultado[1] or "TIMEOUT" in resultado[1]]
    print(f"\nResumen de tests fallidos ({len(tests_fallidos)} tests fallidos):")
    for index, (celular, resultado) in enumerate(tests_fallidos, start=1):
        print(f"{index}. Prueba 'Celular - {celular}': {resultado}")

    # Mostrar resultados exitosos
    print("\nResultados exitosos:")
    for resultado in resultados_celular:
        if resultado not in tests_fallidos:
            print(f"Prueba 'Celular - {resultado[0]}': {resultado[1]}")

except Exception as ex:
    print(f"Error general: {ex}")

print("")
