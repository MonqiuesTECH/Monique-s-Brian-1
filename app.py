import os
import chainlit as cl
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from .env if running locally
load_dotenv()

# Initialize client using Groq's free tier endpoint
client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

MODEL_NAME = "llama-3.3-70b-versatile"

@cl.on_chat_start
async def start_chat():
    cl.user_session.set("message_history", [
        {"role": "system", "content": "You are JARVIS, a hyper-intelligent, precise, and concise AI assistant."}
    ])
    await cl.Message(content="Systems online. How can I assist you today, Boss?").send()

@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("message_history")
    history.append({"role": "user", "content": message.content})
    
    msg = cl.Message(content="")
    await msg.send()

    try:
        stream = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=history,
            stream=True
        )
        
        full_response = ""
        async for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            full_response += token
            await msg.stream_token(token)
            
        history.append({"role": "assistant", "content": full_response})
        cl.user_session.set("message_history", history)
        
    except Exception as e:
        await cl.Message(content=f"Error connecting to model backend: {str(e)}").send()
