import time
import random
import json
from paho.mqtt import client as mqtt_client
import os

MQTT_BROKER = os.getenv('MQTT_BROKER', 'mosquitto')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
DEVICE_ID = 'iot_device_001'

topics = [
    'iot/temperature',
    'iot/humidity', 
    'iot/security/alert'
]

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            for topic in topics:
                client.subscribe(topic)
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client

def simulate_device_data():
    while True:
        data = {
            'device_id': DEVICE_ID,
            'timestamp': time.time(),
            'temperature': random.uniform(20, 30),
            'humidity': random.uniform(40, 60),
            'security_status': random.choice(['safe', 'suspicious'])
        }
        
        print(f"Sending IoT data: {data}")
        time.sleep(5)

if __name__ == "__main__":
    print("Starting IoT Device Simulator...")
    client = connect_mqtt()
    client.loop_start()
    simulate_device_data()

