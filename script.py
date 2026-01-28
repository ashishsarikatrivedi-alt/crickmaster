import os
import google.generativeai as genai
import feedparser

# 1. Setup Gemini with the latest stable model
api_key = os.getenv("GEMINI_KEY")
if not api_key:
    print("Error: GEMINI_KEY not found in Secrets!")
    exit(1)

genai.configure(api_key=api_key)
# Using gemini-1.5-flash for better stability
model = genai.GenerativeModel('gemini-1.5-flash')

def update_site():
    # 2. Get the latest Cricket News
    feed = feedparser.parse("https://news.google.com/rss/search?q=IPL+Cricket+India&hl=en-IN&gl=IN&ceid=IN:en")
    if not feed.entries:
        print("No news found")
        return
    
    new_title = feed.entries[0].title
    
    # 3. Ask Gemini to write the summary
    prompt = f"Write a 100-word punchy cricket news summary for: {new_title}. Focus on IPL and Indian fans."
    response = model.generate_content(prompt)
    ai_summary = response.text

    # 4. Open index.html and replace placeholders
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # These match the text in your beautiful ESPN design
    if "Can India Retain" in html:
        html = html.replace("Can India Retain the Border-Gavaskar Trophy?", new_title)
        html = html.replace("Our automated analysis indicates a significant shift...", ai_summary)
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Success: index.html updated with AI news!")
    else:
        print("Warning: Could not find placeholder text in index.html")

if __name__ == "__main__":
    update_site()
