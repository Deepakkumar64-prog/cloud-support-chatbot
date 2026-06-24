import streamlit as st
from google import genai

st.set_page_config(
    page_title="AWS Cloud Support Assistant",
    page_icon="☁️",
    layout="centered"
)

st.title("☁️ AWS Cloud Support Assistant")
st.caption("Ask questions about AWS services, cloud operations, and troubleshooting.")

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are an AWS Cloud Support Assistant.

Answer in simple and clear language.
Focus on AWS services, cloud operations, troubleshooting, security, monitoring,
cost optimization, and DevOps concepts.

When providing technical steps:
- Use numbered steps.
- Mention important AWS security best practices.
- Do not ask users to share passwords, access keys, secret keys, or sensitive data.
- If the question is unclear, ask one short clarification question.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask an AWS question...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            conversation = [
                {
                    "role": "user",
                    "parts": [{"text": SYSTEM_PROMPT}]
                }
            ]

            for message in st.session_state.messages:
                conversation.append(
                    {
                        "role": message["role"],
                        "parts": [{"text": message["content"]}]
                    }
                )

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=conversation
            )

            answer = response.text
            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
