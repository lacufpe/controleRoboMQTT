import ssl
import paho.mqtt.client as mqtt
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# Configurações do Broker MQTT
MQTT_BROKER = 'aeb92820898a46f9ac54b16138b489ec.s1.eu.hivemq.cloud'
MQTT_PORT = 8883
USERNAME = "robot"  # Substitua pelo usuário
PASSWORD = "Robot111"  # Substitua pela senha
TOPIC_ROBOT_COMMANDS = 'robot/commands'
TOPIC_ROBOT_STATUS = 'robot/status'

# Conectar ao CoppeliaSim
client = RemoteAPIClient()
sim = client.require('sim')

# Variáveis globais para o robô no CoppeliaSim
robot_handle = None
left_motor = None
right_motor = None

def initialize_simulation():
    global robot_handle, left_motor, right_motor
    
    # Inicializar conexão com CoppeliaSim
    # sim.simxFinish(-1)  # Fechar conexões anteriores
    # client_id = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
    print(client)
    if client != -1:
        print("Conectado ao CoppeliaSim")
        
        # Obter handles dos motores (substitua pelos nomes corretos no seu modelo)
        left_motor = sim.getObjectHandle('./DynamicLeftJoint')
        right_motor = sim.getObjectHandle('./DynamicRightJoint')
        print(left_motor,right_motor)
        
        return client
    else:
        print("Falha na conexão com CoppeliaSim")
        return None

# Funções de controle do robô
def move_forward():
    # Definir velocidade dos motores para mover para frente
    sim.setJointTargetVelocity(left_motor, 1.0)
    sim.setJointTargetVelocity(right_motor, 1.0)

def turn_right():
    # Definir velocidade dos motores para virar à direita
    sim.setJointTargetVelocity(left_motor, 1.0)
    sim.setJointTargetVelocity(right_motor, -1.0)


def stop():
    # Parar motores
    sim.setJointTargetVelocity(left_motor, 0.0)
    sim.setJointTargetVelocity(right_motor, 0.0)

# Funções MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com código de resultado {rc}")
    client.subscribe(TOPIC_ROBOT_COMMANDS)

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Comando recebido: {command}")
    
    # Executar comando no robô virtual
    if command == 'MOVE_FORWARD':
        move_forward()
    elif command == 'TURN_RIGHT':
        turn_right()
    elif command == 'STOP':
        stop()

# Inicialização
left_motor = sim.getObjectHandle('./DynamicLeftJoint')
right_motor = sim.getObjectHandle('./DynamicRightJoint')
print("Handles dos motores: {}, {}.".format(left_motor,right_motor))
sim.startSimulation()

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
    if client is not None:
        sim.stopSimulation()
    client.disconnect()
