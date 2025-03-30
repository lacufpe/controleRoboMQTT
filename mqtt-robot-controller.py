# Servidor Python (Publisher/Subscriber)
import ssl
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import time

# Configurações do Broker MQTT
MQTT_BROKER = 'aeb92820898a46f9ac54b16138b489ec.s1.eu.hivemq.cloud'  # IP do seu broker MQTT (pode ser local ou em nuvem)
MQTT_PORT = 8883
TOPIC_ROBOT_COMMANDS = 'robot/commands'
TOPIC_ROBOT_STATUS = 'robot/status'
USERNAME = "robot"  # Substitua pelo usuário
PASSWORD = "Robot111"  # Substitua pela senha

# Função de conexão
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com código de resultado {rc}")
    # Subscrever em tópicos após conexão
    client.subscribe(TOPIC_ROBOT_STATUS)

# Função para processar mensagens recebidas
def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

# Criar cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_NONE)  # Usa TLS para conexão segura

client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Enviar comandos para o robô
def send_robot_command(command):
    client.publish(TOPIC_ROBOT_COMMANDS, command)

# Exemplo de uso
try:
    # Inicia o loop de comunicação
    client.loop_start()
    time.sleep(3)
    # Enviar alguns comandos de exemplo
    print("em frente")
    send_robot_command('MOVE_FORWARD')
    time.sleep(2)
    send_robot_command('TURN_RIGHT')
    time.sleep(0.8)
    send_robot_command('MOVE_FORWARD')
    time.sleep(2)
    send_robot_command('TURN_RIGHT')
    time.sleep(0.8)
    send_robot_command('MOVE_FORWARD')
    time.sleep(2)
    send_robot_command('TURN_RIGHT')
    time.sleep(0.8)
    send_robot_command('MOVE_FORWARD')
    time.sleep(2)
    send_robot_command('TURN_RIGHT')
    time.sleep(0.8)
    send_robot_command('STOP')

    # Manter o programa rodando
    client.loop_forever()

except KeyboardInterrupt:
    print("Encerrando comunicação")
    client.disconnect()
