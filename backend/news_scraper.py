import feedparser
from urllib.parse import quote_plus


def fetch_google_news(topic: str) -> str:
    if not topic or not topic.strip():
        return "No official news available."

    query = quote_plus(topic)
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(rss_url)

    if not feed.entries:
        return "No official news available."

    headlines = []
    for entry in feed.entries[:10]:
        if entry.title:
            headlines.append(entry.title)

    if not headlines:
        return "No official news available."

    return "\n".join(headlines)
