import os
import subprocess

# Directorio base de los scripts de prueba
base_dir = "C:\\Users\\santiago.gauna\\Desktop\\Webdriver\\Fomulario\\Validaciones de campos"

# Lista de scripts de prueba
test_scripts = [
    # "campo_categoria.py",
    # "campo_carrera.py",
    # "campo_consulta.py",
    "campo_email.py",
    "campo_nombre.py",
    "campo_phone.py",
]

# Función para ejecutar los scripts de prueba y contar tests fallidos
def ejecutar_scripts_y_contar_fallidos():
    tests_fallidos = []
    tests_exitosos = []

    for script in test_scripts:
        print(f"Ejecutando {script}...")
        try:
            # Construir la ruta completa al script usando os.path.join()
            ruta_script = os.path.join(base_dir, script)
            
            # Ejecutar el script como un proceso subprocess de Python
            result = subprocess.run(["python", ruta_script], capture_output=True, text=True)
            
            # Analizar la salida del script para determinar si falló
            if "Resumen de tests fallidos" in result.stdout:
                tests_fallidos.append((script, result.stdout))
            else:
                tests_exitosos.append(script)

        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar {script}: {e}")

    # Imprimir resumen de tests fallidos
    print("\nResumen de tests fallidos:")
    if tests_fallidos:
        for index, (script, especificacion) in enumerate(tests_fallidos, start=1):
            print("\n")
            print(f"{index}. {script}:")
            # Mostrar únicamente la parte de los tests fallidos del resultado
            inicio = especificacion.find("Resumen de tests fallidos")
            fin = especificacion.find("Resumen de tests exitosos")
            print(especificacion[inicio:fin].strip())
    else:
        print("No se encontraron tests fallidos.")

    # Imprimir resumen de tests exitosos
    print("\nResumen de tests exitosos:")
    if tests_exitosos:
        for index, script in enumerate(tests_exitosos, start=1):
            print(f"{index}. {script}: Ejecutado correctamente.")
    else:
        print("No se encontraron tests exitosos.")

# Ejecutar los scripts de prueba y contar tests fallidos
if __name__ == "__main__":
    ejecutar_scripts_y_contar_fallidos()
