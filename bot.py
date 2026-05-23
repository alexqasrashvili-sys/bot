import requests
import os
from datetime import date

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

def get_fintech_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "fintech OR payments OR neobank OR digital banking",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json().get("articles", [])

def format_message(articles):
    today = date.today().strftime("%B %d, %Y")
    message = f"📰 Fintech & Payments News — {today}\n\n"
    for i, article in enumerate(articles[:5], 1):
        title = article.get("title", "No title")
        url = article.get("url", "")
        source = article.get("source", {}).get("name", "Unknown")
        message += f"{i}. {title}\n{url}\n{source}\n\n"
    message += "💡 Stay ahead in fintech!"
    return message

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }
    r = requests.post(url, json=payload)
    print("Sent!" if r.ok else f"Error: {r.text}")

if __name__ == "__main__":
    articles = get_fintech_news()
    if articles:
        send_to_telegram(format_message(articles))
    else:
        print("No articles found.")
