import streamlit as st
import requests

# Page config

st.set_page_config(page_title="LLaMA Chat", page_icon="🦙", layout="wide")

st.title("🦙 LLaMA Chat (Local Ollama)")

# Sidebar

with st.sidebar:
st.header("⚙ Settings")
model = st.selectbox("Model", ["llama3.2:1b"])
temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.slider("Max Tokens", 50, 1024, 512)

# Chat history

if "messages" not in st.session_state:
st.session_state.messages = []

# Show previous messages

for msg in st.session_state.messages:
with st.chat_message(msg["role"]):
st.markdown(msg["content"])

# Input box

prompt = st.chat_input("Type your message...")

if prompt:
# Show user message
st.session_state.messages.append({"role": "user", "content": prompt})
with st.chat_message("user"):
st.markdown(prompt)

```
# Generate response
with st.chat_message("assistant"):
    response_placeholder = st.empty()

    try:
        res = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
        )

        data = res.json()
        reply = data.get("response", "⚠ No response from model")

    except Exception as e:
        reply = f"❌ Error: {e}"

    response_placeholder.markdown(reply)

# Save assistant response
st.session_state.messages.append({"role": "assistant", "content": reply})
```
