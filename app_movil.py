import streamlit as st
import requests

st.set_page_config(page_title="Radiografía API", page_icon="🔍")
st.title("🔍 Diagnóstico de Google API Key")

if "GOOGLE_API_KEY" in st.secrets:
    # El .strip() elimina cualquier espacio en blanco accidental que hayas copiado
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    
    st.info("Intentando conectar con los servidores de Google...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    
    try:
        r = requests.get(url, timeout=10)
        
        if r.status_code == 200:
            datos = r.json()
            modelos = datos.get("models", [])
            
            if len(modelos) > 0:
                st.success(f"✅ ¡Éxito! Tu llave tiene acceso a {len(modelos)} modelos.")
                st.write("### Modelos disponibles para ti:")
                for m in modelos:
                    # Filtramos para mostrar solo los que sirven para generar texto
                    if "generateContent" in m.get("supportedGenerationMethods", []):
                        st.code(m.get("name"))
            else:
                st.error("⚠️ La llave es válida, pero tu cuenta de Google NO TIENE NINGÚN MODELO ASIGNADO (0 modelos).")
                st.write("Esto significa que debes crear un proyecto nuevo en Google AI Studio o usar otra cuenta de Gmail.")
                
        else:
            st.error(f"❌ Error devuelto por Google: {r.status_code}")
            st.json(r.json())
            
    except Exception as e:
        st.error(f"❌ Error de red interno: {str(e)}")
else:
    st.error("⚠️ NO SE ENCUENTRA LA LLAVE. Asegúrate de haberla puesto en los 'Secrets' (Misterios) de Streamlit.")
