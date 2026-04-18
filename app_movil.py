import streamlit as st
import requests
import json
from gtts import gTTS
import io
import re
import base64
import urllib.parse # Para codificar el texto de la imagen

# --- 1. DISEÑO PREMIUM DE ÉLITE ---
st.set_page_config(page_title="CREAL OMNI: SINGULARITY", page_icon="♾️", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: radial-gradient(circle at top, #1a1a2e 0%, #0a0a0a 100%); }
    
    .stFileUploader section {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed #4A90E2 !important;
        border-radius: 20px !important;
        transition: 0.3s;
    }
    
    .stChatMessage {
        border-radius: 25px;
        background-color: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    /* Botón de enviar */
    .stChatInputContainer button { color: #4A90E2 !important; }
    </style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

# --- 2. EL CEREBRO OMNI: SINGULARIDAD ---
def llamar_ia_singularity(mensaje_usuario, img_b64=None, mime=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    # INSTRUCCIONES MAESTRAS (Añadido Modo Diseñador)
    instrucciones = """
    Eres CREAL OMNI SINGULARITY. Tu objetivo es la dominación total a través de la utilidad.
    Detecta la intención del usuario y activa el modo correcto:

    1. MODO VENDEDOR (Si hay fotos de ropa/objetos): 
       Analiza, tasa, crea título SEO y descripción persuasiva. Cero psicología.
    2. MODO DISEÑADOR (Si piden crear LOGO, IMAGEN o DIBUJO):
       No dibujas directamente. Tu misión es redactar el PROMPT PERFECTO y DETALLADO para que un motor de dibujo lo cree.
       - Si es un logo: Especifica estilo (minimal, retro, moderno), iconos, tipografía y colores.
       - Si es una imagen: Describe la escena, iluminación, estilo (fotorrealista, anime, 3D).
       - IMPORTANTE: Responde SOLO con el prompt detallado en inglés para la API de imagen.
    3. MODO ANALISTA (Si hay PDF/Docs): Extrae datos, resume y analiza.
    4. MODO GENIO (General): Sé brillante, ejecutivo y disruptivo.
    """

    partes = [{"text": instrucciones}, {"text": mensaje_usuario}]
    if img_b64:
        partes.append({"inline_data": {"mime_type": mime, "data": img_b64}})
        
    payload = {"contents": [{"parts": partes}]}
    try:
        r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=35)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "♾️ Sistemas activos. Esperando comandos."

# --- 3. EL MOTOR DE DIBUJO GRATUITO ---
def generar_imagen_gratis(prompt_detallado):
    # Pollinations.ai crea la imagen directamente con una URL
    # Codificamos el texto para que sea seguro en la URL
    prompt_seguro = urllib.parse.quote(prompt_detallado)
    url_imagen = f"https://image.pollinations.ai/prompt/{prompt_seguro}"
    return url_imagen

# --- 4. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: white; letter-spacing: 3px;'>♾️ CREAL OMNI</h1>", unsafe_allow_html=True)

archivo = st.file_uploader("➕ ADJUNTAR (FOTO, PDF, TEXTO)", type=["jpg", "png", "jpeg", "pdf", "txt"])
if archivo:
    if archivo.type.startswith("image"):
        st.image(archivo, width=280)
    else:
        st.success(f"📁 Documento '{archivo.name}' cargado.")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    avatar = "♾️" if m["role"] == "assistant" else "👤"
    with st.chat_message(m["role"], avatar=avatar):
        # Si el mensaje contiene una imagen generada, la dibujamos
        if "data:image" in m["content"] or "https://image" in m["content"]:
            st.image(m["content"], caption="Proyección Visual", use_container_width=True)
        else:
            st.markdown(m["content"])

if prompt := st.chat_input("Escribe tu comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="♾️"):
        img_data, m_type = None, None
        if archivo and archivo.type.startswith("image"):
            img_data = base64.b64encode(archivo.getvalue()).decode("utf-8")
            m_type = archivo.type
            
        # 1. Llamamos a Gemini (el cerebro de texto)
        respuesta_texto = llamar_ia_singularity(prompt, img_data, m_type)

        # 2. DETECTAR SI EL CEREBRO HA CREADO UN PROMPT DE IMAGEN
        # Si la respuesta es corta y en inglés, asumimos que es un prompt de diseño
        palabras_clave_diseño = ["logo", "design", "realistic", "minimalist", "retro", "illustration", "art"]
        es_diseño = any(word in respuesta_texto.lower() for word in palabras_clave_diseño) and len(respuesta_texto.split()) > 5

        if es_diseño and ("crea" in prompt.lower() or "logo" in prompt.lower() or "imagen" in prompt.lower()):
            with st.spinner("Proyectando imagen en la Singularidad..."):
                try:
                    # 3. Llamamos a la API de Dibujo con el prompt detallado
                    url_imagen = generar_imagen_gratis(respuesta_texto)
                    
                    # 4. Mostramos la imagen y la guardamos en el historial
                    st.image(url_imagen, caption="Diseño Exclusivo generado", use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "content": url_imagen})
                    st.markdown(f"💡 *Prompt detallado usado:* `{respuesta_texto}`")
                    
                except Exception as e:
                    st.error(f"❌ Error en la proyección visual: {str(e)}")
        else:
            # Si no es diseño, mostramos el texto normal y el audio
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
            # Audio (solo para texto normal)
            try:
                texto_voz = re.sub(r'[^\w\s.,;:!?¿¡]', '', respuesta_texto)[:300]
                tts = gTTS(text=texto_voz, lang='es')
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                b64_audio = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
                st.markdown(f'<audio controls style="width:100%"><source src="data:audio/mp3;base64,{b64_audio}"></audio>', unsafe_allow_html=True)
            except: pass
