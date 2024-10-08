# Send Emails
# MQTT Client for CPU Monitoring

This project, developed by **Group 9** , is an MQTT client that monitors CPU usage and sends email alerts when the CPU exceeds a 40% usage threshold. The client also publishes messages to MQTT topics to report system status.

## Features

- **MQTT Communication**: Connects to an MQTT broker (HiveMQ) and publishes system information.
- **CPU Monitoring**: Monitors CPU usage in real-time using `psutil`.
- **Email Alerts**: Sends an alert email if the CPU usage exceeds 40%.

### Topics
- **prueba1**: For receiving data.
- **prueba2**: For sending alerts.

## Prerequisites

- **Python 3.x**
- Required libraries:
  - `paho-mqtt`
  - `psutil`
  - `smtplib`
  - `ssl`

To install these dependencies, run:

```bash
pip install paho-mqtt psutil
