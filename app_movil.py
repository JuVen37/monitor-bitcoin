import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64

# --- 1. CONFIGURACIÓN Y DISEÑO CSS ---
st.set_page_config(page_title="CREAL OMNI", page_icon="🌌", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stChatInputContainer {padding-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
else:
    st.error("⚠️ Faltan las claves en la sección de Misterios de Streamlit.")
    st.stop()

# --- NUEVO MOTOR CON VISIÓN ARTIFICIAL ---
def hablar_con_gemini(mensaje, imagen_base64=None, mime_type=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    partes = [{"text": mensaje}]
    
    if imagen_base64:
        partes.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": imagen_base64
            }
        })
        
    payload = {"contents": [{"parts": partes}]}
    headers = {'Content-Type': 'application/json'}
    
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=25)
        if r.status_code == 200:
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"🚫 Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"❌ Error de red: {str(e)}"

# --- 2. INTERFAZ GRÁFICA PRINCIPAL ---
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌌 CREAL OMNI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Asistente IA - Edición Vinted Pro 👗👕</p>", unsafe_allow_html=True)
st.divider()

with st.sidebar:
    st.title("📸 Analizador Vinted")
    nombre = st.text_input("¿Cómo te llamas?", "Usuario")
    st.markdown("---")
    
    foto_subida = st.file_uploader("Sube la foto de la prenda:", type=["jpg", "jpeg", "png"])
    
    if foto_subida:
        st.success("✅ Foto cargada")
        st.image(foto_subida, caption="Prenda a analizar", use_container_width=True)
        
    st.markdown("---")
    st.caption("Desarrollado por Juan 🚀")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Sube una foto de tu prenda en el menú de la izquierda, dime la marca o detalles, y te crearé el anuncio perfecto **incluyendo una estimación de precio**. 💸"}
    ]

for m in st.session_state.messages:
    avatar_icon = "🌌" if m["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(m["role"], avatar=avatar_icon): 
        st.markdown(m["content"])

if p := st.chat_input("Ej: 'Es una chaqueta Zara talla M casi nueva'"):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user", avatar="🧑‍💻"): 
        st.markdown(p)

    with st.chat_message("assistant", avatar="🌌"):
        with st.spinner("Analizando mercado y creando anuncio..."):
            
            # --- EL NUEVO CEREBRO TASADOR DE VINTED ---
            prompt_vinted = f"""
            Eres un experto tasador de moda y vendedor top en Vinted. El usuario {nombre} quiere vender una prenda.
            Actúa como su asistente personal de marketing. 
            Su mensaje extra es: "{p}".
            Si hay una imagen adjunta, mírala detalladamente para deducir el tipo de tejido, el estilo y la calidad aparente.
            Genera una respuesta súper estructurada que incluya obligatoriamente estas 4 partes:
            
            1. 📝 **TÍTULO:** Un título llamativo y optimizado con palabras clave para que salga el primero en el buscador.
            2. ✍️ **DESCRIPCIÓN:** Una descripción persuasiva (estado, cómo queda puesto, medidas estimadas, con qué combinarlo).
            3. 💰 **PRECIO RECOMENDADO:** Analiza la marca, el tipo de prenda y el mercado actual. Dale un rango de precio de venta realista (ejemplo: entre 12€ y 18€) y explícale brevemente tu razonamiento.
            4. 🏷️ **HASHTAGS:** Lista de 5-10 hashtags útiles.
            
            Usa emojis y un tono amigable, animando a la venta.
            """
            
            imagen_b64 = None
            mime = None
            
            if foto_subida is not None:
                bytes_data = foto_subida.getvalue()
                imagen_b64 = base64.b64encode(bytes_data).decode("utf-8")
                mime = foto_subida.type

            res = hablar_con_gemini(prompt_vinted, imagen_b64, mime)
            st.markdown(res)
            
            if "🚫" not in res and "❌" not in res:
                try:
                    texto_limpio = re.sub(r'[^\w\s.,;:!?¿¡]', '', res)
                    if len(texto_limpio.strip()) > 0:
                        tts = gTTS(text=texto_limpio[:250], lang='es')
                        archivo_en_ram = io.BytesIO()
                        tts.write_to_fp(archivo_en_ram)
                        archivo_en_ram.seek(0)
                        base64_audio = base64.b64encode(archivo_en_ram.read()).decode("utf-8")
                        audio_html = f'''
                            <div style="margin-top: 10px; padding: 10px; border-radius: 10px; background-color: rgba(128, 128, 128, 0.1);">
                                <audio controls style="width: 100%; height: 40px;">
                                    <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3">
                                </audio>
                            </div>
                        '''
                        st.markdown(audio_html, unsafe_allow_html=True)
                except Exception as e:
                    pass

    st.session_state.messages.append({"role": "assistant", "content": res})
