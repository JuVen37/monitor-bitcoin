import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64

# --- 1. CONFIGURACIÓN Y DISEÑO CSS ---
# Ponemos la página centrada y con título oficial
st.set_page_config(page_title="CREAL OMNI", page_icon="🌌", layout="centered")

# CSS Mágico para ocultar marcas de Streamlit y hacerla parecer una App nativa
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stChatInputContainer {padding-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# Verificación de llaves
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
else:
    st.error("⚠️ Faltan las claves en la sección de Misterios de Streamlit.")
    st.stop()

def hablar_con_gemini(mensaje):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": mensaje}]}]}
    headers = {'Content-Type': 'application/json'}
    
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        if r.status_code == 200:
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"🚫 Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"❌ Error de red: {str(e)}"

# --- 2. INTERFAZ GRÁFICA PRINCIPAL ---
# Título centrado con HTML
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌌 CREAL OMNI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Tu Asistente de Inteligencia Artificial Avanzado</p>", unsafe_allow_html=True)
st.divider()

# Menú lateral (Sidebar) rediseñado
with st.sidebar:
    st.title("⚙️ Configuración")
    nombre = st.text_input("¿Cómo te llamas?", "Usuario")
    st.markdown("---")
    st.info("💡 **Cómo funciona:** Escribe cualquier cosa y CREAL generará una respuesta en texto y voz al instante.")
    st.markdown("---")
    st.caption("Desarrollado por Juan 🚀")

# --- 3. HISTORIAL Y CHAT ---
# Inicializamos el historial con un mensaje de bienvenida automático
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy **CREAL OMNI**, tu asistente virtual avanzado. ¿En qué te puedo ayudar hoy?"}
    ]

# Dibujamos los mensajes anteriores con Avatares
for m in st.session_state.messages:
    avatar_icon = "🌌" if m["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(m["role"], avatar=avatar_icon): 
        st.markdown(m["content"])

# --- 4. MOTOR DE RESPUESTA ---
if p := st.chat_input("Escribe tu mensaje aquí..."):
    # Mostramos mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user", avatar="🧑‍💻"): 
        st.markdown(p)

    # Mostramos respuesta de la IA
    with st.chat_message("assistant", avatar="🌌"):
        # Le decimos a la IA el nombre del usuario para que sea más personal
        res = hablar_con_gemini(f"El usuario se llama {nombre}. Responde a esto: {p}")
        st.markdown(res)
        
        if "🚫" not in res and "❌" not in res:
            with st.spinner("Generando voz..."):
                try:
                    texto_limpio = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)
                    if len(texto_limpio.strip()) > 0:
                        # Generación de audio
                        tts = gTTS(text=texto_limpio[:250], lang='es')
                        archivo_en_ram = io.BytesIO()
                        tts.write_to_fp(archivo_en_ram)
                        archivo_en_ram.seek(0)
                        
                        base64_audio = base64.b64encode(archivo_en_ram.read()).decode("utf-8")
                        
                        # Reproductor HTML envuelto en una caja decorativa
                        audio_html = f'''
                            <div style="margin-top: 10px; padding: 10px; border-radius: 10px; background-color: rgba(128, 128, 128, 0.1);">
                                <audio controls style="width: 100%; height: 40px;">
                                    <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3">
                                </audio>
                            </div>
                        '''
                        st.markdown(audio_html, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Error interno al generar audio: {str(e)}")

    # Guardamos la respuesta en el historial
    st.session_state.messages.append({"role": "assistant", "content": res})
