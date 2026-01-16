import requests
from bs4 import BeautifulSoup
from backend.config import settings
from urllib.parse import quote_plus


def fetch_google_news(topic: str) -> str:
    if not topic or not topic.strip():
        return "No topic provided."

    url = f"https://news.google.com/search?q={quote_plus(topic)}&hl=en-US"

    payload = {
        "zone": settings.BRIGHTDATA_ZONE,
        "url": url,
        "format": "raw"
    }

    headers = {
        "Authorization": f"Bearer {settings.BRIGHTDATA_API_KEY}"
    }

    try:
        res = requests.post(
            "https://api.brightdata.com/request",
            json=payload,
            headers=headers,
            timeout=30
        )

        # -------- SAFETY CHECKS --------
        if res.status_code != 200:
            return "No official news available."

        if not res.text or len(res.text.strip()) < 100:
            return "No official news available."

        soup = BeautifulSoup(res.text, "html.parser")

        headlines = []
        for h in soup.find_all("h3"):
            text = h.get_text(strip=True)
            if text:
                headlines.append(text)

        if not headlines:
            return "No official news available."

        return "\n".join(headlines[:10])

    except Exception as e:
        return f"News fetch failed: {str(e)}"
