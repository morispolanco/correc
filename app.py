import streamlit as st
import requests
import json
import docx

# Función para cargar el documento docx
def cargar_documento(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Función para resumir el texto usando la API de Tune
def resumir_con_tune(texto, porcentaje):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['tune']['api_key']}",
        "Content-Type": "application/json"
    }
    
    # Calcular max_tokens basado en el porcentaje
    max_tokens = int(19451 * (porcentaje / 100))
    
    payload = {
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
                "content": "Eres un corrector de textos\n"
            },
            {
                "role": "user",
                "content": f"Resumir este texto: {texto}"
            }
        ],
        "model": "meta/llama-3.1-8b-instruct",
        "stream": False,
        "frequency_penalty": 0,
        "max_tokens": max_tokens
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        resultado = response.json()
        return resultado['choices'][0]['message']['content']
    else:
        st.error("Error al conectarse con la API")
        return None

# Interfaz de Streamlit
st.title("App para resumir documentos DOCX")

# Cargar el documento .docx
archivo_subido = st.file_uploader("Sube un archivo .docx", type=["docx"])

# Porcentaje de resumen solicitado
porcentaje_resumen = st.slider("Selecciona el porcentaje del resumen", 10, 100, 50)

if archivo_subido is not None:
    st.write("Documento cargado:")
    texto_original = cargar_documento(archivo_subido)
    st.text_area("Texto original", texto_original, height=300)

    if st.button("Resumir"):
        with st.spinner("Generando resumen..."):
            resumen = resumir_con_tune(texto_original, porcentaje_resumen)
            if resumen:
                st.subheader("Resumen")
                st.write(resumen)
