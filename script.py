import os
from google import genai
import feedparser
import sys

# 1. Setup the Gemini Client
# It will use your GEMINI_KEY from GitHub Secrets
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

def update_site():
    try:
        # 2. Get the latest Cricket News
        print("Fetching news...")
        feed = feedparser.parse("https://news.google.com/rss/search?q=IPL+Cricket+India&hl=en-IN&gl=IN&ceid=IN:en")
        
        if not feed.entries:
            print("No news entries found.")
            return
        
        new_title = feed.entries[0].title
        print(f"New Headline Found: {new_title}")
        
        # 3. Use the latest 2026 model: gemini-3-flash-preview
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=f"Write a 100-word news summary for this headline: {new_title}. Focus on IPL fans."
        )
        ai_summary = response.text

        # 4. Open and update index.html
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()

        # Placeholders from your design
        title_tag = "Can India Retain the Border-Gavaskar Trophy?"
        desc_tag = "Our automated analysis indicates a significant shift..."

        if title_tag in html:
            html = html.replace(title_tag, new_title)
            html = html.replace(desc_tag, ai_summary)
            
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("✅ Successfully updated index.html with AI news!")
        else:
            print("❌ Error: Could not find placeholder text in HTML.")

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_site()
