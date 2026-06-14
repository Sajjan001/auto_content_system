import requests
import hashlib
import time

def search_image(topic):
    try:
        query = topic.split(':')[0].strip()[:50]
        
        timestamp = int(time.time())
        image_url = f"https://picsum.photos/800/400?random={timestamp}"
        
        print(f"Generated Image URL: {image_url}")
        return image_url
    except Exception as e:
        print(f"Image error: {e}")
        return "https://picsum.photos/800/400?random=default"
