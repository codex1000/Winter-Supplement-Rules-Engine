import json
import logging
import paho.mqtt.client as mqtt
from rules_engine import WinterSupplementRulesEngine

# MQTT Broker Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
INPUT_TOPIC_TEMPLATE = "BRE/calculateWinterSupplementInput/{}"
OUTPUT_TOPIC_TEMPLATE = "BRE/calculateWinterSupplementOutput/{}"

class MQTTHandler:
    def __init__(self, topic_id):
        self.client = mqtt.Client()
        self.topic_id = topic_id
        self.input_topic = INPUT_TOPIC_TEMPLATE.format(topic_id)
        self.output_topic = OUTPUT_TOPIC_TEMPLATE.format(topic_id)

    def connect(self):
        """Set up MQTT connection and event handlers."""
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_BROKER, MQTT_PORT)

    def on_connect(self, client, userdata, flags, rc):
        """Handle the MQTT connection event."""
        if rc == 0:
            logging.info(f"Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
            self.subscribe_to_topic()
        else:
            logging.error(f"Failed to connect, return code {rc}")

    def subscribe_to_topic(self):
        """Subscribe to the current input topic."""
        self.client.subscribe(self.input_topic)
        logging.info(f"Subscribed to topic: {self.input_topic}")

    def on_message(self, client, userdata, message):
        """Handle incoming MQTT messages."""
        logging.info(f"Received message on {message.topic}: {message.payload.decode()}")
        try:
            # Process incoming data
            data = json.loads(message.payload.decode())
            result = WinterSupplementRulesEngine.calculate_supplement(data)
            # Publish result to the output topic
            self.client.publish(self.output_topic, json.dumps(result))
            logging.info(f"Published result to topic: {self.output_topic}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")

    def run(self):
        """Start the MQTT client loop."""
        logging.info("Starting MQTT client loop")
        self.client.loop_forever()