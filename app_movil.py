import streamlit as st
import google.generativeai as genai
import requests
from gtts import gTTS

# --- 1. CONFIGURACIÓN ---
GOOGLE_API_KEY = "AIzaSyAgR4Uw2AFjiZoKb2DiXY2BmGV8HTrU2xc"

def iniciar_sistema():
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        # Usamos el nombre más estable posible
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return None

model = iniciar_sistema()

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

if p := st.chat_input("Escribe 'Hola' para probar..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)

    with st.chat_message("assistant"):
        try:
            # Intentamos generar contenido
            response = model.generate_content(f"Usuario {nombre} dice: {p}")
            res = response.text
        except Exception as e:
            # Si falla, este mensaje nos dirá la VERDAD de lo que pasa
            error_msg = str(e)
            if "429" in error_msg:
                res = "⏳ Google dice que estamos haciendo demasiadas peticiones. Espera un poco."
            elif "403" in error_msg:
                res = "🚫 La clave no tiene permisos todavía. Revisa que el proyecto en Google AI Studio tenga la Facturación (aunque sea gratis) aceptada."
            else:
                res = f"⚠️ Error técnico: {error_msg}. Prueba a reiniciar la app en Streamlit Cloud."

        st.markdown(res)
        
        if st.button("🔊 Audio"):
            tts = gTTS(text=res[:200], lang='es')
            tts.save("voice.mp3")
            token = "8761770621:AAF1WKM_Cz8PPZ1dzro49VLsHdrrnCfZdXc"
            requests.post(f"https://api.telegram.org/bot{token}/sendAudio?chat_id={tele_id}", files={'audio': open("voice.mp3", "rb")})
            st.success("✅ Enviado")

    st.session_state.messages.append({"role": "assistant", "content": res})
