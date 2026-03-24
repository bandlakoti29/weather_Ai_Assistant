from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage

from tools import get_weather, get_forecast, convert_c_to_f

import os
import re
from dotenv import load_dotenv

load_dotenv()

# 🔥 LLM (you can switch to Gemini if needed)
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
    max_retries = 2
)

# 🧰 Tools
tools = [get_weather, get_forecast, convert_c_to_f]

# 🤖 Agent
agent = create_agent(
    model=llm,
    tools=tools,
 system_prompt = """
You are a strict weather assistant.

RULES (VERY IMPORTANT):

1. If the user asks about weather or forecast:
   - ALWAYS call the appropriate tool (get_weather or get_forecast).
   - DO NOT answer from your own knowledge.

2. ONLY return the tool output.
   - Do NOT add explanations.
   - Do NOT give suggestions (like clothing, advice, etc.).
   - Do NOT rephrase or modify the tool result.

3. Do NOT convert units unless user explicitly asks.

4. If tool fails:
   - Return the tool error message directly.

5. Keep response SHORT and EXACT.

6. Never hallucinate data.

Your job is to act like a weather API chatbot.
"""
)

# 🧠 Manual Memory
chat_history = []

# 🔍 Smart city extractor
def extract_city(query: str) -> str:
    match = re.search(r"in ([A-Za-z ]+)", query)
    if match:
        return match.group(1).strip()
    return query.split()[-1]  # fallback


# 🧠 Intelligence Layer
def intelligent_response(query: str):
    global chat_history

    # Add user message
    chat_history.append(HumanMessage(content=query))

    # Invoke agent
    response = agent.invoke({
        "messages": chat_history
    })

    # 🧠 Handle response safely
    msg = response["messages"][-1].content

    # Handle Gemini structured output
    if isinstance(msg, list):
        output = msg[0]["text"]
    else:
        output = msg

    # 🚨 FALLBACK FIX (CRITICAL)
    if "cannot fetch" in output.lower() or "sorry" in output.lower():
        city = extract_city(query)
        output = get_weather.run(city)

    # Add AI response to memory
    chat_history.append(AIMessage(content=output))

    # 🔥 Smart suggestions
    if "°C" in output:
        try:
            temp = float([s for s in output.split() if "°C" in s][0].replace("°C", ""))

            if temp > 35:
                output += "\n🔥 It's very hot. Stay hydrated!"
            elif temp < 10:
                output += "\n❄️ It's cold. Wear warm clothes!"
        except:
            pass

    return output