import streamlit as st
import time
from agent import intelligent_response

st.set_page_config(
    page_title="Weather AI Assistant",
    page_icon="🌦️",
    layout="centered"
)

st.title("🌦️ Weather AI Assistant")
st.caption("Ask about current weather, forecasts, or temperature conversions")

# 🧹 Clear Chat Button
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []

# 🧠 UI Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 💬 Display Chat Messages
for role, message in st.session_state.chat_history:
    avatar = "🧑" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message)

# 📝 Chat Input
user_input = st.chat_input("Ask something like 'Weather in Delhi'...")

if user_input:
    # Show user message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # Assistant response
    with st.chat_message("assistant", avatar="🤖"):

        # ⏳ Animated delay messages
        placeholder = st.empty()
        for msg in ["🌍 Fetching weather...", "☁️ Checking sky...", "🌡️ Getting temperature..."]:
            placeholder.markdown(msg)
            time.sleep(0.4)

        # 🔥 Get response
        response = intelligent_response(user_input)

        # ❌ Remove loading text
        placeholder.empty()

        # 🎭 Add emojis
        response = response.replace("Temperature", "🌡️ Temperature")
        response = response.replace("Humidity", "💧 Humidity")
        response = response.replace("Weather", "☁️ Weather")
        response = response.replace("Feels Like", "🤗 Feels Like")

        # ✅ Show final response
        st.markdown(response)

    # Save history
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", response))