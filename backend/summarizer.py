from backend.llm_groq import groq_summarize


def generate_summary(topic: str, news: str | None = None, reddit: str | None = None) -> str:
    """
    Generate a clean text summary from news and/or reddit content.
    Always returns a safe string (never None).
    """

    # -------- Defensive guards --------
    if not topic or not topic.strip():
        return "No topic provided."

    news_text = news.strip() if isinstance(news, str) and news.strip() else "No official news available."
    reddit_text = reddit.strip() if isinstance(reddit, str) and reddit.strip() else "No Reddit discussions available."

    prompt = f"""
You are a professional broadcast journalist.

Topic:
{topic}

Official News:
{news_text}

Reddit Discussions:
{reddit_text}

Write a clear, factual, and concise news-style summary.
Do not use markdown, bullet points, or emojis.
Keep the length suitable for a short read (roughly 60–90 seconds).
Start directly with the content.
"""

    try:
        summary = groq_summarize(prompt)

        # -------- Final validation --------
        if not summary or not summary.strip():
            return "Summary could not be generated at this time."

        return summary.strip()

    except Exception as e:
        # Never crash Streamlit
        return f"Summary generation failed: {str(e)}"
