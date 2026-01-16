import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    BRIGHTDATA_API_KEY = os.getenv("BRIGHTDATA_API_KEY")
    BRIGHTDATA_ZONE = os.getenv("BRIGHTDATA_ZONE")
    ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

settings = Settings()
