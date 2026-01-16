from groq import Groq
from backend.config import settings
import time
from typing import Optional

# -----------------------------
# Configuration
# -----------------------------
MODEL_ID = "llama-3.1-8b-instant"
TEMPERATURE = 0.3
MAX_TOKENS = 600
RETRIES = 2
RETRY_DELAY_SEC = 0.5


# -----------------------------
# Public API
# -----------------------------
def groq_summarize(
    prompt: str,
    system_message: Optional[str] = None
) -> str:
    """
    Generate a concise text summary using Groq LLM.
    Always fails gracefully (safe for Streamlit Cloud).
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing. Check Streamlit secrets.")

    client = Groq(api_key=settings.GROQ_API_KEY)

    sys_msg = system_message or (
        "You are a professional news analyst who writes concise, factual summaries. "
        "Use simple language, neutral tone, and avoid markdown."
    )

    last_error = None

    for attempt in range(1, RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )

            content = response.choices[0].message.content
            if not content or not content.strip():
                raise RuntimeError("Empty response from Groq model.")

            return content.strip()

        except Exception as e:
            last_error = e
            if attempt < RETRIES:
                time.sleep(RETRY_DELAY_SEC)

    raise RuntimeError(
        f"Groq summarization failed after {RETRIES} attempts: {last_error}"
    )
