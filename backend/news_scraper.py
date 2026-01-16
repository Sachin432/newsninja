import requests
from bs4 import BeautifulSoup
from backend.config import settings
from urllib.parse import quote_plus


def fetch_google_news(topic: str) -> str:
    if not topic or not topic.strip():
        return "No official news available."

    search_query = f"{topic} latest"
    url = f"https://news.google.com/search?q={quote_plus(search_query)}&hl=en-IN&gl=IN&ceid=IN:en"

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
            return "No official news available."

        soup = BeautifulSoup(res.text, "html.parser")

        headlines = []

        # Google News reliable structure (2025)
        for article in soup.find_all("article"):
            title_tag = article.find("h4") or article.find("h3")
            if title_tag:
                text = title_tag.get_text(strip=True)
                if text:
                    headlines.append(text)

        if not headlines:
            return "No official news available."

        return "\n".join(headlines[:10])

    except Exception:
        return "No official news available."
