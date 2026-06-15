import feedparser
import random

FALLBACK_TOPICS = [
    "Artificial Intelligence in Healthcare",
    "The Rise of Large Language Models",
    "Quantum Computing Breakthroughs",
    "Cybersecurity Best Practices for Tech Teams",
    "The Future of Web Development and Edge APIs"
]

FEED_URLS = [
    "https://trends.google.com/trending/rss?geo=US",
    "https://trends.google.com/trending/rss?geo=IN",
    "https://news.ycombinator.com/rss",
    "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=en-IN&gl=IN&ceid=IN:en"
]

def fetch_trends():
    for url in FEED_URLS:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                return random.choice([e.title for e in feed.entries])
        except Exception:
            pass
    return random.choice(FALLBACK_TOPICS)