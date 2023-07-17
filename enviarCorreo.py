################################################################################################ 
####################################### CLIENTE MQTT ########################################### 
################################################################################################

from paho.mqtt import client as mqtt_client
from email.message import EmailMessage
import time
import random
import json
import ssl
import smtplib
import psutil

def enviar_email(cont):
    email_emisor = 'rlkennet12@gmail.com'
    email_password = 'eqrldhbtfucwukyb'
    email_receptor = 'lizpillajo1912@gmail.com'

    asunto = 'Alerta de uso de CPU'
    cuerpo = 'El uso del cpu a superado el porcentaje > 40 contador:' + str(cont) 

    em = EmailMessage()
    em['From'] = email_emisor
    em['To'] = email_receptor
    em['Subject'] = asunto
    em.set_content(cuerpo)

    contexto = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
        smtp.login(email_emisor, email_password)
        smtp.sendmail(email_emisor, email_receptor, em.as_string())


#Hive
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DATA = "prueba1"
TOPIC_ALERT = "prueba2"
# generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
FLAG_CONNECTED = 0


def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_DATA)
        client.subscribe(TOPIC_ALERT)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def on_message(client, userdata, msg):
    #print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), 
    #topic=msg.topic))
    try:
        print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), 
        topic=msg.topic))
        publish(client,TOPIC_ALERT,msg)               

    except Exception as e:
        print(e)

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    #client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client

#Enviar mensajes
def publish(client,TOPIC,msg): 
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)


client = connect_mqtt()
def run():
    cont = 1
    while True:
        publish(client, TOPIC_ALERT, cont)
        cont = cont + 1
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 40:
            enviar_email(cont)
        client.loop_start()
        time.sleep(1)
        if FLAG_CONNECTED:
            print("Wait for message...")
        else:
            client.loop_stop()


if __name__ == '__main__':
    run()