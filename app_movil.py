import streamlit as st
import google.generativeai as genai
import requests
from gtts import gTTS

# --- 1. CONFIGURACIÓN DEL CEREBRO ---
GOOGLE_API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"

def cargar_cerebro():
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        # Usamos el nombre de modelo más directo y compatible
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    except:
        return None

model = cargar_cerebro()

# --- 2. APARIENCIA ---
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

if p := st.chat_input("Dime algo para despertar a la IA..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        try:
            # PROCESO DE RESPUESTA
            prompt_final = f"Eres la IA de Creal. Usuario: {nombre}. Responde de forma brillante: {p}"
            response = model.generate_content(prompt_final)
            res = response.text
        except Exception as e:
            res = "⏳ Google está terminando de activar tu clave. Espera 2 minutos y vuelve a escribir. Ya casi está."

        st.markdown(res)
        
        if st.button("🔊 Mandar audio"):
            tts = gTTS(text=res[:200], lang='es')
            tts.save("voice.mp3")
            token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
            requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})
            st.success("✅ Audio enviado")

    st.session_state.messages.append({"role": "assistant", "content": res})
