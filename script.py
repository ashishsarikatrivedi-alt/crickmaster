import os
from google import genai
import feedparser
import sys

# Initialize the new 2026 Client
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

def update_site():
    try:
        # 1. Fetch News
        feed = feedparser.parse("https://news.google.com/rss/search?q=IPL+Cricket+India&hl=en-IN&gl=IN&ceid=IN:en")
        if not feed.entries:
            return
        
        new_headline = feed.entries[0].title
        
        # 2. Use the NEW 2026 stable model name
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=f"Summarize this for IPL fans in 100 words: {new_headline}"
        )
        ai_summary = response.text

        # 3. Write to index.html
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()

        # Placeholders MUST match your HTML exactly
        h_placeholder = "Can India Retain the Border-Gavaskar Trophy?"
        t_placeholder = "Our automated analysis indicates a significant shift..."

        if h_placeholder in html:
            html = html.replace(h_placeholder, new_headline)
            html = html.replace(t_placeholder, ai_summary)
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("✅ Site Updated!")
        else:
            print("❌ Placeholder not found in HTML.")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_site()
