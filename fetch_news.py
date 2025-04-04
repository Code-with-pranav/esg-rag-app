# fetch_news.py (updated)
import requests
import json
from datetime import datetime
import os

# Your NewsAPI key
API_KEY = "ca965e8512ef4b63b4fc76f4a1e1b51f"
NEWS_API_URL = f"https://newsapi.org/v2/everything?q=ESG&apiKey={API_KEY}"

# Output files for streaming
NEWS_OUTPUT_FILE = "esg_news.jsonl"
ESG_OUTPUT_FILE = "esg_stream_output.jsonl"

def fetch_news():
    """Fetch ESG-related news and return formatted data."""
    try:
        response = requests.get(NEWS_API_URL)
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])

            if not articles:
                print("No news articles found.")
                return []

            # Extract relevant data
            formatted_news = []
            for article in articles[:5]:  # Fetch top 5 articles
                source_name = article.get("source", {}).get("name", "Unknown Source")
                if not source_name:  # Ensure source is not empty
                    source_name = "Unknown Source"
                formatted_news.append({
                    "title": article.get("title", "No Title") or "No Title",
                    "description": article.get("description", "No Description") or "No Description",
                    "published_at": article.get("publishedAt", "2023-01-01T00:00:00Z") or "2023-01-01T00:00:00Z",
                    "source": source_name,
                    "url": article.get("url", "#") or "#"
                })
            print(f"✅ Fetched {len(formatted_news)} news articles")
            return formatted_news
        else:
            print(f"❌ Error: Could not fetch news data. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"⚠️ An error occurred while fetching news: {e}")
        return []

def fetch_esg_report():
    """Fetch the latest simulated ESG report from the data folder."""
    try:
        with open("data/coalco.json", "r", encoding="utf-8") as f:
            esg_report = json.load(f)
        print(f"✅ Fetched ESG report: {esg_report}")
        return esg_report
    except FileNotFoundError:
        print("❌ ESG report not found. Run data_simulator.py first.")
        return {}
    except Exception as e:
        print(f"⚠️ An error occurred while fetching ESG report: {e}")
        return {}

def save_to_jsonl(data, output_file):
    """Append data to a JSONL file."""
    with open(output_file, "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")

def combine_and_save_data():
    """Fetch news and ESG report, then save to JSONL files for streaming."""
    news_data = fetch_news()
    esg_report = fetch_esg_report()

    # Save news data to JSONL
    for news_item in news_data:
        save_to_jsonl(news_item, NEWS_OUTPUT_FILE)

    # Save ESG report to JSONL
    if esg_report:
        save_to_jsonl(esg_report, ESG_OUTPUT_FILE)

    print(f"✅ News data saved to {NEWS_OUTPUT_FILE}")
    print(f"✅ ESG report saved to {ESG_OUTPUT_FILE}")

if __name__ == "__main__":
    # Clear existing files to avoid duplicates during testing
    if os.path.exists(NEWS_OUTPUT_FILE):
        os.remove(NEWS_OUTPUT_FILE)
    if os.path.exists(ESG_OUTPUT_FILE):
        os.remove(ESG_OUTPUT_FILE)
    combine_and_save_data()