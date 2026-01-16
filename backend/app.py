from fastapi import FastAPI, HTTPException
from backend.schemas import NewsRequest
from backend.news_scraper import fetch_google_news
from backend.reddit_scraper import fetch_reddit
from backend.summarizer import generate_summary
import traceback

app = FastAPI()


@app.post("/generate-news-summary")
async def generate_news_summary(req: NewsRequest):
    try:
        topic = req.topics[0]

        print("TOPIC:", topic)
        print("SOURCE:", req.source_type)

        news = None
        reddit = None

        if req.source_type in ["news", "both"]:
            print("Fetching news...")
            news = fetch_google_news(topic)

        if req.source_type in ["reddit", "both"]:
            print("Fetching reddit...")
            reddit = fetch_reddit(topic)

        print("Generating summary...")
        summary = generate_summary(topic, news, reddit)

        return {
            "topic": topic,
            "summary": summary
        }

    except Exception as e:
        print("BACKEND ERROR:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
