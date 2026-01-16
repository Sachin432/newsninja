import requests
from backend.config import settings

def fetch_reddit(topic: str) -> str:
    query = f"https://www.reddit.com/search.json?q={topic}&sort=new"
    headers = {"User-Agent": "NewsNinjaBot/1.0"}
    r = requests.get(query, headers=headers, timeout=15)
    data = r.json()

    posts = []
    for c in data["data"]["children"][:5]:
        posts.append(c["data"]["title"])

    return "\n".join(posts)
