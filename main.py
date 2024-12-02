import logging
from mqtt_handler import MQTTHandler
import requests
from bs4 import BeautifulSoup

# Web App Configuration
WEB_APP_URL = "https://winter-supplement-app-d690e5-tools.apps.silver.devops.gov.bc.ca/"
WEB_APP_USERNAME = "user"
WEB_APP_PASSWORD = "r44UKbfSeIn9AZjI4Ed24xr6"

def fetch_topic_id():
    """Log in to the web app and fetch the dynamically generated topic ID."""
    try:
        response = requests.get(
            WEB_APP_URL,
            auth=(WEB_APP_USERNAME, WEB_APP_PASSWORD)
        )
        response.raise_for_status()

        # check if the connection worked
        print(f"Connection successful. Status code: {response.status_code}")
        print("Response content:")
        print(response.text)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting")
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Now instead of fetching the id you ask for it to be typed manually e.g
    topic_id = input("Enter the initial MQTT Topic ID: ").strip()
    handler = MQTTHandler(topic_id)
    handler.connect()

    try:
        handler.run()
    except KeyboardInterrupt:
        logging.info("Exiting MQTT client...")
        handler.client.disconnect()