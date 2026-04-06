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
    device_id = f"device_{random.randint(1,5)}"
    while True:
        data = {
    'Device': device_id,
    'timestamp': time.time(),

    # Environment
    'temperature': random.uniform(20, 35),
    'humidity': random.uniform(30, 70),
    'pressure': random.uniform(990, 1025),

    # Device behavior
    'cpu_usage': random.uniform(10, 90),
    'memory_usage': random.uniform(100, 500),  # MB
    'battery': random.uniform(20, 100),

    # Network behavior
    'packet_rate': random.randint(10, 200),
    'failed_logins': random.randint(0, 5),

    # Security
    'security_status': 'safe'
}
        
        print(f"Sending IoT data: {data}")
        time.sleep(5)

if __name__ == "__main__":
    print("Starting IoT Device Simulator...")
    client = connect_mqtt()
    client.loop_start()
    simulate_device_data()

