import os
from google import genai
import feedparser
import sys

# 1. Setup the new Gemini Client
# It will automatically find your GEMINI_KEY from secrets
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

def update_site():
    try:
        # 2. Get News
        print("Fetching news...")
        feed = feedparser.parse("https://news.google.com/rss/search?q=IPL+Cricket+India&hl=en-IN&gl=IN&ceid=IN:en")
        
        if not feed.entries:
            print("No news found")
            return
        
        new_title = feed.entries[0].title
        print(f"Found: {new_title}")
        
        # 3. Use the latest stable model: gemini-2.0-flash
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"Summarize this cricket news in 100 punchy words for IPL fans: {new_title}"
        )
        ai_summary = response.text

        # 4. Update index.html
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()

        # Placeholders from your ESPN design
        title_placeholder = "Can India Retain the Border-Gavaskar Trophy?"
        text_placeholder = "Our automated analysis indicates a significant shift..."

        if title_placeholder in html:
            html = html.replace(title_placeholder, new_title)
            html = html.replace(text_placeholder, ai_summary)
            
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("✅ Site Updated Successfully!")
        else:
            print("❌ Error: Could not find placeholder text in HTML.")

    except Exception as e:
        print(f"❌ Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_site()
