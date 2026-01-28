import os
from google import genai
import feedparser
import sys

# 1. Setup the new Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

def update_site():
    try:
        # 2. Get the latest Cricket News
        print("Fetching news...")
        feed = feedparser.parse("https://news.google.com/rss/search?q=IPL+Cricket+India&hl=en-IN&gl=IN&ceid=IN:en")
        
        if not feed.entries:
            print("No news entries found.")
            return
        
        new_headline = feed.entries[0].title
        print(f"New Headline: {new_headline}")
        
        # 3. Use the current stable 2.0 model
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"Summarize this cricket news in 100 punchy words for IPL fans: {new_headline}"
        )
        ai_summary = response.text

        # 4. Open and update index.html
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()

        # Placeholders MUST match your HTML exactly
        title_tag = "Can India Retain the Border-Gavaskar Trophy?"
        desc_tag = "Our automated analysis indicates a significant shift..."

        if title_tag in html:
            html = html.replace(title_tag, new_headline)
            html = html.replace(desc_tag, ai_summary)
            
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("✅ Success: index.html updated!")
        else:
            print("❌ Error: Placeholder text not found in index.html. Check your HTML!")

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_site()
