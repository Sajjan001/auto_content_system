import feedparser
import random

def fetch_trends():

    feed = feedparser.parse(
        "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=en-IN&gl=IN&ceid=IN:en"
    )

    topics = []

    for entry in feed.entries[:20]:
        topics.append(entry.title)

    selected_topic = random.choice(topics)
    print(f"Available Trends: {len(topics)}")
    print(f"Selected Topic: {selected_topic}")
    
    return selected_topic