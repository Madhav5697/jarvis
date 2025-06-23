import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

API_KEY = os.getenv("NEWS_API_KEY")

def get_news(category="general", country="in"):
    try:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data["status"] != "ok":
            return "Sir, there was a problem fetching the news."

        articles = data.get("articles", [])[:7]  # Top 5 headlines
        if not articles:
            return "No news found for that category, sir."

        news_summary = ""
        for i, article in enumerate(articles, 1):
            title = article.get("title")
            if title:
                news_summary += f"{i}. {title}\n"

        return news_summary.strip()

    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        return "Apologies sir, I couldn't fetch the news right now."
