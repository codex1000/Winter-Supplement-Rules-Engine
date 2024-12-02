import unittest
from unittest.mock import patch, MagicMock
import json
from rules_engine import WinterSupplementRulesEngine
from mqtt_handler import MQTTHandler

class TestWinterSupplementRulesEngine(unittest.TestCase):

    def test_calculate_supplement_eligible_single(self):
        data = {
            "id": "123",
            "numberOfChildren": 0,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        }
        expected_result = {
            "id": "123",
            "isEligible": True,
            "baseAmount": 60.0,
            "childrenAmount": 0.0,
            "supplementAmount": 60.0
        }
        result = WinterSupplementRulesEngine.calculate_supplement(data)
        self.assertEqual(result, expected_result)

    def test_calculate_supplement_eligible_couple(self):
        data = {
            "id": "123",
            "numberOfChildren": 0,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
        expected_result = {
            "id": "123",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 0.0,
            "supplementAmount": 120.0
        }
        result = WinterSupplementRulesEngine.calculate_supplement(data)
        self.assertEqual(result, expected_result)

    def test_calculate_supplement_eligible_family_with_children(self):
        data = {
            "id": "123",
            "numberOfChildren": 2,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
        expected_result = {
            "id": "123",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 40.0,
            "supplementAmount": 160.0
        }
        result = WinterSupplementRulesEngine.calculate_supplement(data)
        self.assertEqual(result, expected_result)

    def test_calculate_supplement_not_eligible(self):
        data = {
            "id": "123",
            "numberOfChildren": 2,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": False
        }
        expected_result = {
            "id": "123",
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0
        }
        result = WinterSupplementRulesEngine.calculate_supplement(data)
        self.assertEqual(result, expected_result)

class TestMQTTHandler(unittest.TestCase):

    @patch('paho.mqtt.client.Client')
    def test_mqtt_handler_connect(self, MockClient):
        mock_client_instance = MockClient.return_value
        mock_client_instance.connect = MagicMock()

        handler = MQTTHandler("test_topic_id")
        handler.connect()

        mock_client_instance.connect.assert_called_once_with("test.mosquitto.org", 1883)
        self.assertEqual(mock_client_instance.on_connect, handler.on_connect)
        self.assertEqual(mock_client_instance.on_message, handler.on_message)

    @patch('paho.mqtt.client.Client')
    def test_mqtt_handler_on_connect(self, MockClient):
        mock_client_instance = MockClient.return_value
        mock_client_instance.subscribe = MagicMock()

        handler = MQTTHandler("test_topic_id")
        handler.on_connect(mock_client_instance, None, None, 0)

        mock_client_instance.subscribe.assert_called_once_with("BRE/calculateWinterSupplementInput/test_topic_id")

    @patch('paho.mqtt.client.Client')
    def test_mqtt_handler_on_message(self, MockClient):
        mock_client_instance = MockClient.return_value
        mock_client_instance.publish = MagicMock()

        handler = MQTTHandler("test_topic_id")
        message = MagicMock()
        message.topic = "BRE/calculateWinterSupplementInput/test_topic_id"
        message.payload = json.dumps({
            "id": "123",
            "numberOfChildren": 2,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }).encode('utf-8')

        handler.on_message(mock_client_instance, None, message)

        expected_result = {
            "id": "123",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 40.0,
            "supplementAmount": 160.0
        }
        mock_client_instance.publish.assert_called_once_with("BRE/calculateWinterSupplementOutput/test_topic_id", json.dumps(expected_result))

if __name__ == '__main__':
    unittest.main()
