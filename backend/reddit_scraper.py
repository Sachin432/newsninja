import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from backend.config import settings


def fetch_reddit(topic: str) -> str:
    """
    Fetch recent Reddit discussion titles using Bright Data.
    Returns newline-separated post titles.
    """

    if not topic or not topic.strip():
        return "No Reddit discussions available."

    # Reddit search URL (HTML, not JSON)
    url = f"https://www.reddit.com/search/?q={quote_plus(topic)}&sort=new"

    payload = {
        "zone": settings.BRIGHTDATA_ZONE,
        "url": url,
        "format": "raw"
    }

    headers = {
        "Authorization": f"Bearer {settings.BRIGHTDATA_API_KEY}"
    }

    try:
        response = requests.post(
            "https://api.brightdata.com/request",
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code != 200 or not response.text:
            return "No Reddit discussions available."

        soup = BeautifulSoup(response.text, "html.parser")

        posts = []

        # Reddit post titles are inside <h3> tags
        for h3 in soup.find_all("h3"):
            text = h3.get_text(strip=True)
            if text:
                posts.append(text)

        posts = posts[:5]

        if not posts:
            return "No Reddit discussions available."

        return "\n".join(posts)

    except Exception:
        return "No Reddit discussions available."
