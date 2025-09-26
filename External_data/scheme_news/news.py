import re
import json
from transformers import pipeline

articles = []

with open(r"C:\SIH_BACKEND\External_data\scheme_news\output2\news.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Extract articles
matches = re.findall(
    r"TITLE:\s*(.*?)\n\nCONTENT:\s*(.*?)(?=\n\nKEYWORDS:|\n\n=+|\Z)", 
    text, 
    re.S
)

for title, content in matches:
    articles.append({
        "title": title.strip(),
        "content": content.strip().replace("\n", " ")
    })

labels = ["Harmful for farmers", "Neutral", "Positive for farmers"]
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

harmful_articles = []

for art in articles:
    text = art["title"] + " " + art["content"]
    output = classifier(text, candidate_labels=labels)
    
    # Filter only harmful news
    if output["labels"][0] == "Harmful for farmers":
        harmful_articles.append({
            "title": art["title"],
            "content": art["content"],
            "scores": dict(zip(output["labels"], output["scores"]))
        })

# Save to JSON file
output_path = r"C:\SIH_BACKEND\External_data\scheme_news\output2\news.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(harmful_articles, f, indent=4, ensure_ascii=False)

print(f"Saved harmful articles to {output_path}")
print(f"Total harmful articles: {len(harmful_articles)}")
