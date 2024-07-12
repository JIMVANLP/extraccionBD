from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configura las opciones del navegador (opcional)
options = Options()
options.add_argument("--start-maximized")  # Ejemplo de configuración adicional

# Configura el servicio del ChromeDriver con la ruta al ejecutable
service = Service('C:\\Users\\Admin\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')


# Inicializa el navegador Chrome con el servicio y opciones configuradas
driver = webdriver.Chrome(service=service, options=options)

# Ahora puedes usar el navegador como lo necesites
driver.get("http://www.google.com")

# Cierra el navegador al finalizar
driver.quit()

