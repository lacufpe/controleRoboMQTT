#include <WiFi.h>
#include <PubSubClient.h>
#include "RoboCore_Vespa.h"

// Configurações WiFi
const char* WIFI_SSID = "Mecatronica";
const char* WIFI_PASSWORD = "Mec@tr0n";

// Configurações do HiveMQ Cloud
const char* MQTT_BROKER = "aeb92820898a46f9ac54b16138b489ec.s1.eu.hivemq.cloud"; // Substitua pelo seu host
const int MQTT_PORT = 8883; // Porta TLS segura
const char* MQTT_USER = "your-username"; // Substitua pelo usuário
const char* MQTT_PASSWORD = "your-password"; // Substitua pela senha

WiFiClientSecure espClient;  // Cliente com TLS
PubSubClient client(espClient); 

const char* TOPIC_ROBOT_COMMANDS = "robot/commands";
const char* TOPIC_ROBOT_STATUS = "robot/status";

// Configurações Vespa
VespaServo servo1;
int servo1Pos;

void setupWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado ao WiFi");
}

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    if (mqttClient.connect("ESP32Client")) {
      Serial.println("Conectado ao broker MQTT");
      mqttClient.subscribe(TOPIC_ROBOT_COMMANDS);
      mqttClient.publish(TOPIC_ROBOT_STATUS, "Robô Online");
    } else {
      delay(5000);
    }
  }
}

void MQTTcallback(char* topic, byte* message, unsigned int length) {
  String messageTemp;
  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }

  if (String(topic) == TOPIC_ROBOT_COMMANDS) {
    if (messageTemp == "MOVE_FORWARD") {
      // Lógica para mover para frente
      Serial.println("Movendo para frente");
    } else if (messageTemp == "TURN_RIGHT") {
      // Lógica para virar à direita
      Serial.println("Virando à direita");
    } else if (messageTemp == "STOP") {
      // Lógica para parar
      Serial.println("Parando");
    }
  }
}

void setup() {
  Serial.begin(115200);
  setupWiFi();
  
  espClient.setInsecure(); // Para ignorar verificação de certificado TLS
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(MQTTcallback);

  servo1.attach(VESPA_SERVO_S1,700,2400); // servo on pin 26, with default min and max
  servo1.write(servo1Pos);
}

void loop() {
  if (!mqttClient.connected()) {
    reconnectMQTT();
  }
  mqttClient.loop();
}
