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

        if res.status_code != 200 or not res.text:
            return "No news available."

        soup = BeautifulSoup(res.text, "html.parser")

        headlines = [
            h.get_text(strip=True)
            for h in soup.find_all("h3")
            if h.get_text(strip=True)
        ][:10]

        if not headlines:
            return "No news available."

        return "\n".join(headlines)

    except Exception as e:
        return f"News fetch failed: {str(e)}"
