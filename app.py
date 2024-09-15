import streamlit as st
import requests

def summarize_text(text, percentage, api_key):
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "temperature": 0.8,
        "messages": [
            {
                "role": "system",
                "content": "Eres un corrector de textos\n"
            },
            {
                "role": "user",
                "content": f"Resume el siguiente texto al {percentage}% de su longitud original:\n\n{text}"
            }
        ],
        "model": "meta/llama-3.1-8b-instruct",
        "stream": False,
        "frequency_penalty": 0,
        "max_tokens": 19451
    }

    response = requests.post(
        "https://proxy.tune.app/chat/completions",
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
    st.title("📝 Resumidor de Documentos con Tune API")

    uploaded_file = st.file_uploader("Sube un documento de texto", type=["txt"])
    percentage = st.slider("Selecciona el porcentaje de resumen (%)", 10, 100, 50)

    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        if st.button("Resumir"):
            with st.spinner("Generando resumen..."):
                api_key = st.secrets["api_key"]
                summary = summarize_text(text, percentage, api_key)
            st.subheader("Resumen:")
            st.write(summary)

if __name__ == "__main__":
    main()
