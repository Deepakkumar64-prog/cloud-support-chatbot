import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AWS Chatbot Debug", page_icon="☁️")
st.title("☁️ Debug — Available Models")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.success("API key loaded.")
except Exception as e:
    st.error(f"Secret not found: {e}")
    st.stop()

try:
    genai.configure(api_key=api_key)
    st.subheader("Models available on your API key:")
    models = genai.list_models()
    for m in models:
        if "generateContent" in m.supported_generation_methods:
            st.write(f"✅ {m.name}")
except Exception as e:
    st.error(f"Error listing models: {e}")
