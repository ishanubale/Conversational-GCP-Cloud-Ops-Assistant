import streamlit as st
from agent import run_agent  # Import our backend RAG agent


st.set_page_config(page_title="Conversational CloudOps Assistant", page_icon="☁️")

st.title("☁️ Conversational CloudOps Assistant")
st.write("Your AI helper for Conversational CCAI CloudOps")

# Session state for conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input("Here to help you toubleshooting the demons in CCAI..."):
    # Save user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get LLM response via agent.py
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        response_text = run_agent(prompt)
        msg_placeholder.markdown(response_text)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": response_text})
