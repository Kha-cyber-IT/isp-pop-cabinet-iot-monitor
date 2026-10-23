import network
import time
import ujson
from machine import Pin
import dht
from umqtt.simple import MQTTClient

# Hardware Setup
sensor = dht.DHT22(Pin(15))
alarm_led = Pin(2, Pin.OUT)
alarm_led.value(0)

# Topology & Broker Details (EMQX Public Broker)
SITE_ID      = "soweto-pop-04"
CABINET_ID   = "olt-rack-b"
CLIENT_ID    = f"isp-{SITE_ID}-{CABINET_ID}"
BROKER       = "broker.emqx.io"

BASE_TOPIC   = f"isp/{SITE_ID}/{CABINET_ID}"
TOPIC_DATA   = f"{BASE_TOPIC}/telemetry"
TOPIC_ALERTS = f"{BASE_TOPIC}/alerts"

CRITICAL_TEMP_THRESHOLD = 35.0

# 1. Connect to Wi-Fi Interface
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("[*] Connecting to Access Network...", end="")
        wlan.connect("Wokwi-GUEST", "")
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(0.3)
        print("\n[+] Wi-Fi Attached. IP:", wlan.ifconfig()[0])
    return wlan

# 2. Connect to MQTT Broker
def connect_mqtt():
    print(f"[*] Connecting to {BROKER}...", end="")
    client = MQTTClient(client_id=CLIENT_ID, server=BROKER, port=1883, keepalive=60)
    client.connect()
    print(" Connected!")
    return client

connect_wifi()
mqtt = connect_mqtt()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        
        status = "NORMAL"
        
        # Edge Logic: Overheat check
        if temp >= CRITICAL_TEMP_THRESHOLD:
            status = "CRITICAL_OVERHEAT"
            alarm_led.value(1)
            
            alert = ujson.dumps({
                "severity": "CRITICAL",
                "site": SITE_ID,
                "cabinet": CABINET_ID,
                "temp_c": temp,
                "alert": "Thermal Alarm"
            })
            mqtt.publish(TOPIC_ALERTS, alert)
            print(f"[!] ALARM SENT -> {alert}")
        else:
            alarm_led.value(0)

        telemetry = ujson.dumps({
            "site": SITE_ID,
            "cabinet": CABINET_ID,
            "temp_c": temp,
            "humidity": humidity,
            "status": status
        })
        mqtt.publish(TOPIC_DATA, telemetry)
        print(f"[NOC-METRIC] -> {telemetry}")

    except Exception as e:
        print("[!] Reconnecting MQTT:", e)
        time.sleep(2)
        try:
            connect_wifi()
            mqtt = connect_mqtt()
        except:
            pass

    time.sleep(3)
