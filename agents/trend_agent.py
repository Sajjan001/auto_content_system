import feedparser
import random

def fetch_trends():
    feed_urls = [
        "https://trends.google.com/trending/rss?geo=US",
        "https://trends.google.com/trending/rss?geo=IN",
        "https://news.ycombinator.com/rss",
        "http://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=en-IN&gl=IN&ceid=IN:en"
    ]
    
    topics = []
    for url in feed_urls:
        try:
            print(f"Fetching trends from: {url}")
            feed = feedparser.parse(url)
            if feed.entries:
                topics = [entry.title for entry in feed.entries]
                print(f"Got {len(topics)} topics.")
                break
        except Exception as e:
            print(f"Error fetching from {url}: {e}")

    if not topics:
        fallback_topics = [
            "Artificial Intelligence in Healthcare",
            "The Rise of Large Language Models",
            "Quantum Computing Breakthroughs",
            "Cybersecurity Best Practices for Tech Teams",
            "The Future of Web Development and Edge APIs"
        ]
        selected = random.choice(fallback_topics)
        print(f"Using fallback topic: {selected}")
        return selected

    selected = random.choice(topics)
    print(f"Selected Trend: {selected}")
    return selected