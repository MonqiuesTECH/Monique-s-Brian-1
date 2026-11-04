import os
import chainlit as cl
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load and override environment variables from local .env
load_dotenv(override=True)

# Retrieve and clean the API key string
api_key = os.environ.get("GROQ_API_KEY", "").strip()

if not api_key:
    print("❌ WARNING: GROQ_API_KEY is missing or empty in your .env file!")

# Initialize AsyncOpenAI client targeting Groq's endpoint
client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

MODEL_NAME = "llama-3.1-70b-versatile"

@cl.on_chat_start
async def start_chat():
    # Initialize chat session history with a system prompt
    cl.user_session.set("message_history", [
        {"role": "system", "content": "You are JARVIS, a hyper-intelligent, precise, and concise AI assistant."}
    ])
    await cl.Message(content="Systems online. How can I assist you today, Boss?").send()

@cl.on_message
async def main(message: cl.Message):
    # Fetch existing history and append the new user message
    history = cl.user_session.get("message_history")
    history.append({"role": "user", "content": message.content})
    
    # Create an empty message container for streaming chunks
    msg = cl.Message(content="")
    await msg.send()

    try:
        # Stream response from Groq API
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
            
        # Append assistant response to history
        history.append({"role": "assistant", "content": full_response})
        cl.user_session.set("message_history", history)
        
    except Exception as e:
        await cl.Message(content=f"Error connecting to model backend: {str(e)}").send()
