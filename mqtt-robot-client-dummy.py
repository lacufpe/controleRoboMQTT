import paho.mqtt.client as mqtt
import ssl
import time

# Configurações do Broker MQTT
MQTT_BROKER = 'aeb92820898a46f9ac54b16138b489ec.s1.eu.hivemq.cloud'
MQTT_PORT = 8883
TOPIC_ROBOT_COMMANDS = 'robot/commands'
TOPIC_ROBOT_STATUS = 'robot/status'
USERNAME = "robot"  # Substitua pelo usuário
PASSWORD = "Robot111"  # Substitua pela senha

# Funções de controle do robô
def move_forward():
    print("Avante!")

def turn_right():
    print("Não podia ser para a esquerda.")

def stop():
    print("Apenas uma pausa.")

# Funções MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com código de resultado {rc}")
    client.subscribe(TOPIC_ROBOT_COMMANDS)

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Comando recebido: {command}")
    
    if command == 'MOVE_FORWARD':
        move_forward()
    elif command == 'TURN_RIGHT':
        turn_right()
    elif command == 'STOP':
        stop()


# Configurar cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_NONE)  # Usa TLS para conexão segura
client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    # Iniciar loop de comunicação
    client.loop_start()

    # Manter o programa rodando
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Encerrando comunicação")
    client.disconnect()
