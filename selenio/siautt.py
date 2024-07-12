from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configura las opciones del navegador (opcional)
options = Options()
options.add_argument("--start-maximized")  # Abre la ventana del navegador maximizada

# Configura el servicio del ChromeDriver con la ruta al ejecutable
service = Service('C:\\Users\\Admin\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')


# Inicializa el navegador Chrome con el servicio y opciones configuradas
driver = webdriver.Chrome(service=service, options=options)

# Abre la página de inicio de sesión de Uttorreon
driver.get("https://uttorreon.mx/")

try:
    # Espera hasta que el elemento de inicio de sesión esté presente y visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )

    # Encuentra el campo de usuario y escribe tu nombre de usuario
    username_field = driver.find_element(By.ID, "email")
    username_field.send_keys("zadoc.ilp@gmail.com")  # Reemplaza con tu nombre de usuario

    # Encuentra el campo de contraseña y escribe tu contraseña
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("Katana750")  # Reemplaza con tu contraseña

    # Envía el formulario de inicio de sesión
    password_field.send_keys(Keys.RETURN)

    # Espera a que se cargue la página después del inicio de sesión (puedes usar un elemento específico como prueba)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_del_elemento_que_indica_que_ha_iniciado_sesion"))
    )

    # Ejemplo: obtener el título de la página después de iniciar sesión
    print("Título de la página después de iniciar sesión:", driver.title)

except Exception as e:
    print("Error durante el inicio de sesión:", str(e))

finally:
    # Cierra el navegador al finalizar
    driver.quit()
