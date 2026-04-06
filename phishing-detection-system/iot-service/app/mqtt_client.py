from paho.mqtt import client as mqtt_client
import json
import os

class IoTMQTTClient:
    def __init__(self, broker=os.getenv('MQTT_BROKER', 'localhost'), port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt_client.Client()
        self.client.on_message = self.on_message
        
    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        print(f"Received MQTT message: {payload}")
        # Trigger security check if suspicious
        if payload.get('security_status') == 'suspicious':
            print("🚨 IoT security alert!")
    
    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
    
    def publish(self, topic, data):
        self.client.publish(topic, json.dumps(data))

# Usage
if __name__ == "__main__":
    client = IoTMQTTClient()
    client.connect()

