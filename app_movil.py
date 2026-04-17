import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime
import pytz
import random

# --- CONFIGURACIÓN ---
TOKEN_TELEGRAM = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
ID_USUARIO = "8449303559"

# --- INTERFAZ ---
st.set_page_config(page_title="IA TOTAL CREAL", page_icon="🌐", layout="wide")

# Estilo Neón Premium
st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stMetric { background: linear-gradient(135deg, #111, #222); border: 1px solid #00ffc8; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DATOS (Mantenemos lo anterior) ---
def obtener_luz():
    try:
        r = requests.get("https://api.preciodelaluz.org/v1/prices/all?zone=PCB").json()
        h = datetime.now(pytz.timezone('Europe/Madrid')).strftime("%H") + "-24"
        return r[h]['price'] / 1000
    except: return 0.15

def obtener_btc():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
        return float(r['bitcoin']['usd'])
    except: return 70000.0

# --- DASHBOARD ---
st.title("🌐 SISTEMA DE INTELIGENCIA TOTAL")
luz = obtener_luz()
btc = obtener_btc()

col1, col2 = st.columns(2)
col1.metric("ESTADO LUZ", f"{luz:.4f} €")
col2.metric("BITCOIN", f"${btc:,.0f}")

st.divider()

# --- CHAT MULTI-PROPÓSITO (ESTILO CHATGPT) ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hola, soy la IA de Creal. Puedes hablar conmigo de finanzas, de tus sentimientos o de lo que se te ocurra. ¡Soy todo oídos!"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Escribe lo que quieras..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        p = prompt.lower()
        
        # 1. Lógica Financiera
        if "luz" in p or "precio" in p:
            res = f"La luz está ahora a {luz:.4f}€. ¿Quieres que te avise si baja más?"
        elif "bitcoin" in p or "btc" in p:
            res = f"El BTC está a ${btc:,.0f}. El mercado nunca duerme, ¿tienes alguna estrategia en mente?"
        
        # 2. Lógica de Psicólogo/Empatía
        elif any(w in p for w in ["triste", "mal", "ayuda", "estres", "solo"]):
            res = "Aquí me tienes. No eres solo números para mí; tu bienestar es lo primero. Cuéntame más, te escucho."
        
        # 3. CONVERSACIÓN GENERAL (El "Cerebro" abierto)
        elif any(w in p for w in ["que eres", "quien eres", "haces"]):
            res = "Soy una IA creada por Creal. Mi misión es vigilar el mundo por ti y ser el compañero con el que siempre puedes contar."
        elif any(w in p for w in ["puedes", "sabes"]):
            res = "¡Puedo hacer de todo! Desde analizar mercados hasta contarte un chiste o filosofar sobre la vida. ¿Qué te apetece probar?"
        elif any(w in p for w in ["clima", "tiempo"]):
            res = "Todavía no tengo mis sensores de clima activados, pero espero que haga un día perfecto para ti."
        
        # 4. Respuesta Aleatoria para conversación fluida
        else:
            respuestas_random = [
                "Esa es una pregunta interesante, cuéntame más sobre eso.",
                "¡Qué curioso! Nunca lo había pensado así. ¿Tú qué opinas?",
                "Me encanta charlar contigo. ¿En qué más estás pensando?",
                "Como IA, siempre estoy aprendiendo cosas nuevas gracias a lo que me cuentas.",
                "¡Vaya! Eso suena genial. Dime, ¿cómo puedo ayudarte hoy con ese tema?"
            ]
            res = random.choice(respuestas_random)

        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
