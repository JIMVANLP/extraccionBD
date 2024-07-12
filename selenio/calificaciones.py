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

# Abre la página de inicio de sesión de Uttorreon
driver.get("https://uttorreon.mx/")

try:
    # Llena el formulario de inicio de sesión
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    username_input.send_keys("zadoc.ilp@gmail.com")  # Reemplaza con tu usuario

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.send_keys("Katana750")  # Reemplaza con tu contraseña

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()

    # Espera hasta que aparezca el enlace "Mi Espacio" y haz clic en él
    mi_espacio_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Mi Espacio')]/parent::a"))
    )
    mi_espacio_link.click()

    # Espera hasta que aparezca el enlace "Académico" y haz clic en él
    academico_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Académico')]/parent::a"))
    )
    academico_link.click()

    # Espera hasta que aparezca el enlace "Mis Calificaciones" y haz clic en él
    mis_calificaciones_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Mis Calificaciones')]/parent::a"))
    )
    mis_calificaciones_link.click()

    # Espera hasta que la tabla de calificaciones esté presente
    tabla_calificaciones = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "Tabla"))
    )

    # Tiempo de espera adicional para asegurar que la tabla esté completamente cargada
    time.sleep(5)

    # Obtiene los encabezados de la tabla
    encabezados = tabla_calificaciones.find_elements(By.XPATH, ".//thead/tr/th")
    encabezados_texto = [encabezado.text.strip() for encabezado in encabezados]

    # Obtiene todas las filas de la tabla de calificaciones
    filas = tabla_calificaciones.find_elements(By.XPATH, ".//tbody/tr")

    # Lista para almacenar los datos de las calificaciones
    calificaciones_data = []

    for fila in filas:
        # Obtén las celdas de cada fila
        celdas = fila.find_elements(By.TAG_NAME, "td")
        fila_datos = [celda.text.strip() for celda in celdas]
        calificaciones_data.append(fila_datos)

    # Crea un DataFrame de pandas con los datos de las calificaciones
    df = pd.DataFrame(calificaciones_data, columns=encabezados_texto)


    # Guarda el DataFrame en un archivo Excel
    df.to_excel("calificaciones.xlsx", index=False)

    print("Calificaciones guardadas en calificaciones.xlsx")

except Exception as e:
    print("Error durante la navegación:", str(e))

finally:
    # Cierra el navegador al finalizar
    driver.quit()
