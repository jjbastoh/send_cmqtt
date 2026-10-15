import streamlit as st
import paho.mqtt.client as mqtt
import json

st.set_page_config(page_title="Control MQTT")
st.title("Control MQTT - ESP32 en Wokwi")

BROKER = "157.230.214.127"
PORT = 1883

# Cliente MQTT de Streamlit
@st.cache_resource
def conectar_mqtt():
    cliente = mqtt.Client(client_id="STREAMLIT_CONTROL")
    cliente.connect(BROKER, PORT, 60)
    cliente.loop_start()
    return cliente

try:
    client1 = conectar_mqtt()
    st.success("Conectado al broker MQTT")

    # Control ON/OFF del LED
    st.subheader("Control del LED")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("ON", use_container_width=True):
            mensaje = json.dumps({"Act1": "ON"})
            info = client1.publish("cmqtt_s", mensaje)
            info.wait_for_publish()
            st.success("Comando ON enviado")

    with col2:
        if st.button("OFF", use_container_width=True):
            mensaje = json.dumps({"Act1": "OFF"})
            info = client1.publish("cmqtt_s", mensaje)
            info.wait_for_publish()
            st.success("Comando OFF enviado")

    # Control del servo mediante un valor analógico
    st.subheader("Control del servomotor")

    values = st.slider(
        "Selecciona el valor",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

    st.write("Valor seleccionado:", values)

    if st.button("Enviar valor analógico"):
        mensaje = json.dumps({"Analog": float(values)})
        info = client1.publish("cmqtt_a", mensaje)
        info.wait_for_publish()
        st.success(f"Valor {values} enviado a Wokwi")

except Exception as e:
    st.error(f"Error de conexión MQTT: {e}")
3. Cambios en el código de Wokwi (sketch.ino)
En tu ESP32 debes identificar el cliente como WOKWI_ESP32 y mantener las suscripciones:

cpp
if (client.connect("WOKWI_ESP32")) {
  Serial.println("Conectado al broker MQTT");

  client.subscribe("cmqtt_s");
  client.subscribe("cmqtt_a");
}
Después, reemplaza o agrega la función callback() para que interprete los mensajes JSON. Tu código ya incluye ArduinoJson, WiFi y ESP32Servo.

cpp

void callback(char* topic, byte* payload,
              unsigned int length) {

  // Convertir el mensaje recibido en texto
  char mensaje[201];

  if (length >= sizeof(mensaje)) {
    Serial.println("Mensaje demasiado largo");
    return;
  }

  memcpy(mensaje, payload, length);
  mensaje[length] = '\0';

  Serial.print("Topico: ");
  Serial.println(topic);

  Serial.print("Mensaje: ");
  Serial.println(mensaje);

  StaticJsonDocument<200> doc;

  DeserializationError error = deserializeJson(doc, mensaje);

  if (error) {
    Serial.println("Error al interpretar JSON");
    return;
  }

  // Topico para encender y apagar el LED
  if (strcmp(topic, "cmqtt_s") == 0) {

    const char* estado = doc["Act1"] | "";

    if (strcmp(estado, "ON") == 0) {
      digitalWrite(2, HIGH);
      Serial.println("LED ENCENDIDO");
    }
    else if (strcmp(estado, "OFF") == 0) {
      digitalWrite(2, LOW);
      Serial.println("LED APAGADO");
    }
  }

  // Topico para controlar el servomotor
  if (strcmp(topic, "cmqtt_a") == 0) {

    if (doc["Analog"].is<float>() ||
        doc["Analog"].is<int>()) {

      float valor = doc["Analog"];
      valor = constrain(valor, 0.0, 100.0);

      int angulo = (int)(valor * 180.0 / 100.0);

      myservo.write(angulo);

      Serial.print("Angulo del servo: ");
      Serial.println(angulo);
    }
  }
}
Asegúrate de que la función setup() incluya:

cpp
client.setServer(mqtt_server, 1883);
client.setCallback(callback);
Y que tu función loop() mantenga viva la conexión:

cpp
void loop() {
  if (!client.connected()) {
    reconnect();
  }

  client.loop();
}



