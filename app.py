import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="AWS Cloud Support Assistant",
    page_icon="☁️",
    layout="centered"
)

st.title("☁️ AWS Cloud Support Assistant")
st.caption("Ask questions about AWS services, cloud operations, and troubleshooting.")

# --- Load API key ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("API key loaded.")
except Exception as e:
    st.error(f"Secret not found: {e}")
    st.stop()

# --- Configure Gemini ---
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="""
        You are an AWS Cloud Support Assistant.
        Answer in simple and clear language.
        Focus on AWS services, cloud operations, troubleshooting, security,
        monitoring, cost optimization, and DevOps concepts.
        When providing technical steps use numbered steps.
        Do not ask users to share passwords, access keys, or sensitive data.
        """
    )
except Exception as e:
    st.error(f"Model load error: {e}")
    st.stop()

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- Display past messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Input ---
question = st.chat_input("Ask an AWS question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            try:
                response = st.session_state.chat.send_message(question)
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Gemini API error: {e}")

# --- Sidebar ---
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    st.rerun()
