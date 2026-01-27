# app.py
import streamlit as st
from LLM_chatbot import ask_chatbot  # import your chatbot function


st.container()
# Title
st.title("📚 LLM Chatbot Interface")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("You:")

if st.button("Send"):
    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get chatbot response
        answer = ask_chatbot(user_input)
        clean_answer = getattr(answer, "content", str(answer))
        st.session_state.messages.append({"role": "assistant", "content": clean_answer})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div style='color:blue'>You: {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='color:green'>Bot: {msg['content']}</div>", unsafe_allow_html=True)
