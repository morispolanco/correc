import streamlit as st
import requests
from docx import Document
import io

def extract_text_from_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def summarize_text(text, percentage, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [
            {
                "role": "user",
                "content": f"Resume el siguiente texto al {percentage}% de su longitud original:\n\n{text}"
            }
        ],
        "max_tokens": 2512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1.0,
        "stop": ["<|eot_id|>"],
        "stream": False
    }

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        result = response.json()
        summary = result['choices'][0]['message']['content']
        return summary.strip()
    else:
        return f"Error {response.status_code}: {response.text}"

def main():
    st.title("📝 Resumidor de Documentos con Together API")

    uploaded_file = st.file_uploader("Sube un documento", type=["docx"])
    percentage = st.slider("Selecciona el porcentaje de resumen (%)", 10, 100, 50)

    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Por favor, sube un archivo .docx válido.")
            return

        if st.button("Resumir"):
            with st.spinner("Generando resumen..."):
                api_key = st.secrets["api_key"]
                summary = summarize_text(text, percentage, api_key)
            st.subheader("Resumen:")
            st.write(summary)

if __name__ == "__main__":
    main()
