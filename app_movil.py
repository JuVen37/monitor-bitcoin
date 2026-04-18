import streamlit as st
import google.generativeai as genai
import requests
from gtts import gTTS

# --- 1. CONFIGURACIÓN ---
GOOGLE_API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"

# Forzamos la configuración a la versión estable
genai.configure(api_key=GOOGLE_API_KEY)

# Función para intentar despertar al modelo sin usar versiones beta
def despertar_ia():
    try:
        # Probamos con el nombre de modelo que NUNCA falla
        return genai.GenerativeModel('gemini-pro')
    except:
        return None

model = despertar_ia()

# --- 2. INTERFAZ ---
st.set_page_config(page_title="CREAL OMNI", page_icon="🌌")
st.markdown("<style>.main { background: #000; color: #00ffc8; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛡️ Nodo Central")
    nombre = st.text_input("Nombre", "Creal")
    tele_id = st.text_input("ID Telegram", "8449303559")

# --- 3. CHAT ---
st.title("🌌 CREAL OMNI-INTELLIGENCE")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Escribe 'Hola' para forzar respuesta..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        try:
            # Mandamos la pregunta ignorando errores de versión
            response = model.generate_content(f"Hola, soy {nombre}. {p}")
            res = response.text
        except Exception as e:
            # Si sale el 404, vamos a imprimir una ayuda visual
            res = f"⚠️ Google sigue reportando error 404. Por favor, ve a Streamlit Cloud y pulsa 'REBOOT APP' ahora mismo. Es vital para limpiar la memoria."

        st.markdown(res)
        
        if st.button("🔊 Audio"):
            tts = gTTS(text=res[:200], lang='es')
            tts.save("voice.mp3")
            token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
            requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})
            st.success("✅ Enviado")

    st.session_state.messages.append({"role": "assistant", "content": res})
