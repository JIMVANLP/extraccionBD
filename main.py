import json
import sys
from web_automator import WebAutomator

def main(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)

    driver_path = config['driver_path']
    actions = config['actions']

    automator = WebAutomator(driver_path)

    try:
        automator.setup_driver()
        automator.perform_actions(actions)
    finally:
        automator.close_driver()

if __name__ == "__main__":
    # Verificar si se pasó un argumento de línea de comandos para la ruta del archivo de configuración
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    main(config_path)