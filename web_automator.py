from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pandas as pd

class WebAutomator:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None

    def setup_driver(self):
        options = Options()
        options.add_argument("--start-maximized")
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def open_url(self, url):
        self.driver.get(url)

    def input_text(self, selector, text):
        element = self._find_element(selector)
        if element:
            element.send_keys(text)

    def click(self, selector):
        element = self._find_element(selector)
        if element:
            element.click()

    def scroll_to_element(self, selector):
        element = self._find_element(selector)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def click_next_page(self, selector):
        next_button = self._find_element(selector)
        if next_button:
            self.driver.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(1)  # Añadir un pequeño retardo para asegurar que el elemento esté completamente visible
            next_button.click()

    def extract_table(self, selector):
        table_element = self._find_element(selector)
        if not table_element:
            print("No se encontró la tabla.")
            return None, None

        headers_text = []
        table_data = []

        # Extraer encabezados
        header_rows = table_element.find_elements(By.XPATH, ".//thead/tr")
        for header_row in header_rows:
            header_cells = header_row.find_elements(By.TAG_NAME, "th")
            row_data = []
            for cell in header_cells:
                colspan = int(cell.get_attribute("colspan") or 1)
                cell_text = cell.text.strip()
                row_data.append(cell_text)
                for _ in range(colspan - 1):
                    row_data.append('')  # Rellenar con cadenas vacías para los colspan adicionales
            headers_text.append(row_data)

        # Extraer datos de las filas
        data_rows = table_element.find_elements(By.XPATH, ".//tbody/tr")
        for row in data_rows:
            row_data = []
            cells = row.find_elements(By.TAG_NAME, "td")
            for cell in cells:
                colspan = int(cell.get_attribute("colspan") or 1)
                cell_text = cell.text.strip()
                row_data.append(cell_text)
                for _ in range(colspan - 1):
                    row_data.append('')  # Rellenar con cadenas vacías para los colspan adicionales
            table_data.append(row_data)

        # Ajustar tamaño de encabezados y datos
        max_columns = max(len(row) for row in headers_text + table_data)
        headers_text = [row + [''] * (max_columns - len(row)) for row in headers_text]
        table_data = [row + [''] * (max_columns - len(row)) for row in table_data]

        return headers_text, table_data

    def save_to_excel(self, headers, data, filename):
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Crear DataFrame combinado para encabezados y datos
            df_headers = pd.DataFrame(headers)
            df_data = pd.DataFrame(data)
            
            # Combinar encabezados y datos
            combined_df = pd.concat([df_headers, df_data], ignore_index=True, sort=False)
            
            # Guardar en la hoja del archivo Excel
            combined_df.to_excel(writer, sheet_name='Datos', index=False, header=False)
        print(f"Información de la tabla guardada en {filename}")

    def perform_actions(self, actions):
        for action in actions:
            print(f"Ejecutando acción: {action['action']}")
            if action["action"] == "open_url":
                self.open_url(action["url"])
            elif action["action"] == "input":
                self.input_text(action["selector"], action["text"])
            elif action["action"] == "click":
                self.click(action["selector"])
            elif action["action"] == "scroll":
                self.scroll_to_element(action["selector"])
            elif action["action"] == "scroll_to_bottom":
                self.scroll_to_bottom()
            elif action["action"] == "click_next_page":
                self.click_next_page(action["selector"])
            elif action["action"] == "select_season":
                self.select_season(action["selector"], action["season_name"])
            elif action["action"] == "click_search":
                self.click(action["selector"])
            elif action["action"] == "extract_table":
                table_selector = action["table_selector"]
                headers_text, table_data = self.extract_table(table_selector)
                if headers_text and table_data:
                    filename = f"tabla_{action['season_name'].replace('/', '-')}.xlsx"
                    self.save_to_excel(headers_text, table_data, filename)
            time.sleep(1)  # Ajustar el tiempo de espera según sea necesario

    def select_season(self, selector, season_name):
        select_element = self._find_element(selector)
        if not select_element:
            print("No se encontró el selector de temporadas.")
            return

        options = select_element.find_elements(By.TAG_NAME, "option")
        for option in options:
            if option.text.strip() == season_name:
                print(f"Seleccionando temporada: {season_name}")
                select_element.click()
                option.click()
                return
        print(f"No se encontró la temporada: {season_name}")

    def _find_element(self, selector):
        try:
            by = selector["by"].upper().replace(" ", "_")
            by = getattr(By, by)
            value = selector["value"]
            print(f"Buscando elemento: {by} = {value}")
            return WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception as e:
            print(f"No se encontró el elemento: {e}")
            return None

def main(config_path):
    with open(config_path, "r") as file:
        config = json.load(file)

    driver_path = config["driver_path"]
    actions = config["actions"]

    automator = WebAutomator(driver_path)
    automator.setup_driver()

    try:
        automator.perform_actions(actions)
    finally:
        automator.close_driver()

if __name__ == "__main__":
    config_path = "config.json"
    main(config_path)
