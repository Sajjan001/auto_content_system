import time

STOP_WORDS = {"in","on","at","to","for","of","and","the","a","an","is","with","as","by","from","how","why","who","what"}

def search_image(topic):
    keywords = [
        w for w in ("".join(c if c.isalnum() else " " for c in topic)).lower().split()
        if w not in STOP_WORDS and len(w) >= 2
    ]
    tags = ",".join(keywords[:3]) or "technology"
    return f"https://loremflickr.com/800/400/{tags}?random={int(time.time())}"
