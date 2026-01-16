from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

print("Groq key loaded:", bool(os.getenv("GROQ_API_KEY")))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",   # ✅ UPDATED MODEL
    messages=[
        {"role": "user", "content": "Say hello in one sentence"}
    ]
)

print("LLM RESPONSE:")
print(response.choices[0].message.content)
