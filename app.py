import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

st.set_page_config(page_title="Cyber Vault | MQTT", page_icon="🔐", layout="wide")

st.markdown("""
<style>
.stApp {
    background: radial-gradient(ellipse at top, #172b43 0%, #080e19 55%, #050912 100%);
    color: #e6f1ff;
}
.block-container {
    padding-top: 2rem;
    max-width: 1150px;
}
h1, h2, h3, p, label {
    color: #e6f1ff;
}
.vault-header {
    text-align: center;
    padding: 22px;
    border: 1px solid #24415c;
    border-radius: 18px;
    background: linear-gradient(135deg, #102239, #0a1423);
    box-shadow: 0 0 30px #00e6aa12;
    margin-bottom: 25px;
}
.vault-title {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: 5px;
    color: #48f5c1;
    margin: 0;
}
.vault-subtitle {
    color: #8faac5;
    letter-spacing: 2px;
    font-size: 12px;
    margin-top: 8px;
}
.vault-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 28px 0;
}
.vault {
    width: 250px;
    height: 250px;
    border-radius: 50%;
    background: radial-gradient(circle, #263e56 0%, #142438 55%, #0a1320 72%);
    border: 8px solid #496781;
    box-shadow: 0 0 0 7px #101e30, 0 0 0 9px #29465e,
                0 0 40px #00e6aa20, inset 0 0 25px #000b17;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}
.vault::before {
    content: "";
    position: absolute;
    inset: 15px;
    border-radius: 50%;
    border: 2px dashed #7190a9;
    animation: vault-spin 24s linear infinite;
}
.vault-wheel {
    width: 155px;
    height: 155px;
    border: 7px solid #8da9bd;
    border-radius: 50%;
    background: radial-gradient(circle, #29435a, #102034);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: inset 0 0 20px #0008, 0 0 18px #0005;
}
.vault-wheel::before {
    content: "";
    position: absolute;
    width: 7px;
    height: 125px;
    background: linear-gradient(to bottom, #9bb6ca 0%, #9bb6ca 45%, transparent 45%, transparent 55%, #9bb6ca 55%);
    border-radius: 5px;
}
.vault-wheel::after {
    content: "";
    position: absolute;
    width: 125px;
    height: 7px;
    background: linear-gradient(to right, #9bb6ca 0%, #9bb6ca 45%, transparent 45%, transparent 55%, #9bb6ca 55%);
    border-radius: 5px;
}
.vault-center {
    z-index: 1;
    width: 68px;
    height: 68px;
    border-radius: 50%;
    background: #102236;
    border: 3px solid #48f5c1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    box-shadow: 0 0 18px #48f5c155;
}
.vault-status {
    text-align: center;
    padding: 15px;
    border-radius: 13px;
    border: 1px solid #28425a;
    background: #101e30;
    margin: 15px 0;
}
.status-light {
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    margin-right: 8px;
}
.locked { color: #ffc56a; }
.locked .status-light { background: #ffc56a; box-shadow: 0 0 12px #ffc56a; }
.unlocked { color: #48f5c1; }
.unlocked .status-light { background: #48f5c1; box-shadow: 0 0 12px #48f5c1; }
@keyframes vault-spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
div.stButton > button {
    border-radius: 10px;
    min-height: 44px;
    border: 1px solid #31536c;
    background: #12243a;
    color: #e6f1ff;
    transition: all .2s ease;
}
div.stButton > button:hover {
    border-color: #48f5c1;
    color: #48f5c1;
    box-shadow: 0 0 15px #48f5c125;
}
.panel {
    background: linear-gradient(145deg, #101e30, #0b1422);
    border: 1px solid #253d55;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}
@media (prefers-reduced-motion: reduce) {
    .vault::before { animation: none; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="vault-header">
  <div class="vault-title">◈ CYBER VAULT</div>
  <div class="vault-subtitle">SISTEMA DE SEGURIDAD · PYTHON + MQTT</div>
</div>
""", unsafe_allow_html=True)

st.write("Versión de Python:", platform.python_version())

values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "157.230.214.127"
port = 1883
client1 = paho.Client("STREAMLIT_APP")
client1.on_message = on_message

st.title("MQTT Control")

col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 ON", use_container_width=True):
        act1 = "ON"
        client1 = paho.Client("STREAMLIT_APP")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("streamlit/led", message)

with col2:
    if st.button("🔴 OFF", use_container_width=True):
        act1 = "OFF"
        client1 = paho.Client("STREAMLIT_APP")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("streamlit/led", message)

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.subheader("🔐 Control de acceso")

values = st.slider(
    "Gira el mecanismo de la bóveda",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    key="vault_slider"
)

rotation = int(values * 3.6)
is_unlocked = values >= 90
vault_class = "unlocked" if is_unlocked else "locked"
vault_text = "DESBLOQUEADA" if is_unlocked else "BLOQUEADA"
vault_icon = "🔓" if is_unlocked else "🔒"

st.markdown(f"""
<div class="vault-wrap">
  <div class="vault">
    <div class="vault-wheel" style="transform:rotate({rotation}deg);">
      <div class="vault-center">{vault_icon}</div>
    </div>
  </div>
</div>
<div class="vault-status {vault_class}">
  <span class="status-light"></span>
  <strong>BÓVEDA {vault_text}</strong><br>
  <small>Ángulo del mecanismo: {rotation}° · Nivel: {values:.0f}%</small>
</div>
""", unsafe_allow_html=True)

st.progress(int(values), text=f"Nivel de apertura: {values:.0f}%")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("📡 Enviar valor analógico", use_container_width=True):
    client1 = paho.Client("STREAMLIT_APP")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("streamlit/servo", message)
    client1.disconnect()
