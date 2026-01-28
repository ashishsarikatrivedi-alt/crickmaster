import os
import google.generativeai as genai
import feedparser

# 1. Setup Gemini with your Key
genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel('gemini-pro')

def update_site():
    # 2. Get the latest Cricket News from Google
    feed = feedparser.parse("https://news.google.com/rss/search?q=IPL+Cricket+India&hl=en-IN&gl=IN&ceid=IN:en")
    
    if not feed.entries:
        print("No news found!")
        return

    top_story_title = feed.entries[0].title
    
    # 3. Ask Gemini to write a summary
    prompt = f"Write a 100-word punchy cricket news summary for: {top_story_title}. Keep it professional and exciting for IPL fans."
    response = model.generate_content(prompt)
    ai_summary = response.text

    # 4. Open index.html and put the new news inside
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # This replaces the placeholder text in the design with REAL AI News
    html = html.replace("Can India Retain the Border-Gavaskar Trophy?", top_story_title)
    html = html.replace("Our automated analysis indicates a significant shift...", ai_summary)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Website updated with latest news!")

if __name__ == "__main__":
    update_site()
