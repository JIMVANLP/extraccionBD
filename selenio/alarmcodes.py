from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Configuración del navegador Chrome
options = Options()
options.add_argument("--start-maximized")  # Inicia el navegador maximizado

# Ruta al ejecutable del ChromeDriver
service = Service('C:\\Users\\Admin\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')

# Inicializa el navegador Chrome con la configuración y el servicio
driver = webdriver.Chrome(service=service, options=options)

# Abre la página con la tabla
driver.get("https://www.cncspares.com/blog/fanuc-alarm-codes/")

try:
    # Espera hasta que la tabla esté presente
    tabla_calificaciones = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )

    # Tiempo de espera adicional para asegurar que la tabla esté completamente cargada
    time.sleep(5)

    # Obtiene los encabezados de la tabla
    encabezados = tabla_calificaciones.find_elements(By.XPATH, ".//thead/tr/th")
    encabezados_texto = [encabezado.text.strip() for encabezado in encabezados]

    # Obtiene todas las filas de la tabla
    filas = tabla_calificaciones.find_elements(By.XPATH, ".//tbody/tr")

    # Lista para almacenar los datos de la tabla
    calificaciones_data = []

    for fila in filas:
        # Obtén las celdas de cada fila
        celdas = fila.find_elements(By.TAG_NAME, "td")
        fila_datos = [celda.text.strip() for celda in celdas]
        calificaciones_data.append(fila_datos)

    # Crea un DataFrame de pandas con los datos de la tabla
    df = pd.DataFrame(calificaciones_data, columns=encabezados_texto)

    # Guarda el DataFrame en un archivo Excel
    df.to_excel("fanuc_alarm_codes.xlsx", index=False)

    print("Datos guardados en fanuc_alarm_codes.xlsx")

except Exception as e:
    print("Error durante la navegación:", str(e))

finally:
    # Cierra el navegador al finalizar
    driver.quit()
