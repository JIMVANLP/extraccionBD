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

# URL de la página web
url = "https://www.cncspares.com/blog/fanuc-alarm-codes/"  # Cambia esta URL a la página que desees

# Abre la página web
driver.get(url)

try:
    # Espera hasta que la tabla esté presente
    tabla = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )

    # Tiempo de espera adicional para asegurar que la tabla esté completamente cargada
    time.sleep(5)

    # Obtiene los encabezados de la tabla
    encabezados = tabla.find_elements(By.XPATH, ".//thead/tr/th")
    encabezados_texto = [encabezado.text.strip() for encabezado in encabezados]

    # Si no hay encabezados, intenta con el primer cuerpo de la tabla
    if not encabezados_texto:
        encabezados = tabla.find_elements(By.XPATH, ".//tbody/tr[1]/td")
        encabezados_texto = [f"Column {i+1}" for i in range(len(encabezados))]

    # Obtiene todas las filas de la tabla
    filas = tabla.find_elements(By.XPATH, ".//tbody/tr")

    # Lista para almacenar los datos de la tabla
    tabla_data = []

    for fila in filas:
        # Obtén las celdas de cada fila
        celdas = fila.find_elements(By.TAG_NAME, "td")
        fila_datos = [celda.text.strip() for celda in celdas]
        tabla_data.append(fila_datos)

    # Crea un DataFrame de pandas con los datos de la tabla
    df = pd.DataFrame(tabla_data, columns=encabezados_texto)

    # Guarda el DataFrame en un archivo Excel
    df.to_excel("tabla_datos.xlsx", index=False)

    print("Datos guardados en tabla_datos.xlsx")

except Exception as e:
    print("Error durante la navegación:", str(e))

finally:
    # Cierra el navegador al finalizar
    driver.quit()
