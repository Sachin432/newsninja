import requests
from backend.config import settings


def fetch_reddit(topic: str) -> str:
    if not topic or not topic.strip():
        return "No topic provided."

    url = f"https://www.reddit.com/search.json?q={topic}&sort=new&limit=5"
    headers = {
        "User-Agent": "NewsNinjaBot/1.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)

        # -------- Status check --------
        if r.status_code != 200 or not r.text:
            return "No Reddit discussions available."

        # -------- Safe JSON parse --------
        try:
            data = r.json()
        except ValueError:
            # Reddit returned HTML / blocked page
            return "No Reddit discussions available."

        children = data.get("data", {}).get("children", [])
        if not children:
            return "No Reddit discussions available."

        posts = []
        for c in children[:5]:
            title = c.get("data", {}).get("title")
            if title:
                posts.append(title)

        if not posts:
            return "No Reddit discussions available."

        return "\n".join(posts)

    except Exception as e:
        return f"Reddit fetch failed: {str(e)}"
