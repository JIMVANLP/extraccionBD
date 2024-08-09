import json
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
    config_path = 'config.json'
    main(config_path)
