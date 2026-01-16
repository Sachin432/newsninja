import requests
from bs4 import BeautifulSoup
from backend.config import settings
from urllib.parse import quote_plus

def fetch_google_news(topic: str) -> str:
    url = f"https://news.google.com/search?q={quote_plus(topic)}&hl=en-US"
    payload = {
        "zone": settings.BRIGHTDATA_ZONE,
        "url": url,
        "format": "raw"
    }
    headers = {"Authorization": f"Bearer {settings.BRIGHTDATA_API_KEY}"}

    res = requests.post(
        "https://api.brightdata.com/request",
        json=payload,
        headers=headers,
        timeout=30
    )
    soup = BeautifulSoup(res.text, "html.parser")
    headlines = [h.text for h in soup.find_all("h3")][:10]
    return "\n".join(headlines)
