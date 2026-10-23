# 📡 ISP POP Cabinet IoT Environmental Monitor

An edge-computing environmental telemetry and alarm node engineered for remote ISP Point of Presence (POP) cabinets and fiber telco racks. Built with an ESP32 microcontroller running MicroPython.

---

### 🔗 Live Interactive Simulation

Test the virtual ESP32 hardware and sensor live directly in your browser:

👉 **[Launch Wokwi Live Project](https://wokwi.com/projects/478603044346822657)**

---

## 🎯 What Problem Does This Solve?

Remote street-level ISP cabinets house critical fiber equipment (OLTs, switches, UPS units). 

* **Overheating:** High temperatures lead to network downtime and damaged line cards.
* **Lack of Visibility:** NOC engineers often only find out about heat spikes when fiber links drop.

**This project solves that:** An automated sensor node constantly checks temperature and humidity, triggers a red warning LED on-site when heat exceeds 35°C, and sends real-time metrics over MQTT to the Network Operations Center (NOC).

---

## ⚙️ Key Features

* **Real-Time Environmental Telemetry:** Reads temperature and relative humidity every 3 seconds via DHT22.
* **Edge Intelligence & Local Alarm:** Automatically lights up a local red warning LED when temperature reaches **>= 35.0°C**.
* **MQTT Telemetry Feed:** Transmits JSON payloads to public broker `broker.emqx.io`.
* **Fault-Tolerant Reconnect:** Recovers Wi-Fi and MQTT transport automatically if signal drops.

---

## 📐 Circuit Wiring & Pinout

| Hardware Component | Component Pin | ESP32 GPIO | Description |
| :--- | :--- | :--- | :--- |
| **DHT22 Sensor** | VCC | 3V3 | 3.3V Power Supply |
| **DHT22 Sensor** | SDA / Data | GPIO 15 | Digital Data Signal |
| **DHT22 Sensor** | GND | GND | Common Ground |
| **Alarm LED** | Anode (+) | GPIO 2 | Connected via 220Ω resistor |
| **Alarm LED** | Cathode (-) | GND | Ground Return |

---

## 🌐 MQTT Topics & Payload Structure

* **Broker:** `broker.emqx.io` (Port 1883)
* **Telemetry Topic:** `isp/soweto-pop-04/olt-rack-b/telemetry`
* **Alert Topic:** `isp/soweto-pop-04/olt-rack-b/alerts`

**Sample JSON Telemetry:**
```json
{
  "site": "soweto-pop-04",
  "cabinet": "olt-rack-b",
  "temp_c": 24.0,
  "humidity": 40.0,
  "status": "NORMAL"
}
