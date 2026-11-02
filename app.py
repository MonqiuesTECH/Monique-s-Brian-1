import os
import chainlit as cl
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# DEBUG: Print the first few characters of the key to your terminal to verify it's loading
raw_key = os.environ.get("GROQ_API_KEY")
print(f"--> DEBUG: Loaded API Key starts with: {str(raw_key)[:6]}..." if raw_key else "--> DEBUG: API Key is NONE/EMPTY!")

# Initialize client using Groq's free tier endpoint
client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=raw_key
)

MODEL_NAME = "llama-3.1-70b-versatile"
