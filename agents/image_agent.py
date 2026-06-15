import time

def search_image(topic):
    try:
        words = topic.lower().split()
        stop_words = {"in", "on", "at", "to", "for", "of", "and", "the", "a", "an", "is", "with", "as", "by", "from", "how", "why", "who", "what"}
        
        keywords = []
        for word in words:
            clean_word = "".join(char for char in word if char.isalnum())
            if clean_word and clean_word not in stop_words and len(clean_word) >= 2:
                keywords.append(clean_word)
        
        tag_list = keywords[:3] if keywords else ["technology"]
        tags = ",".join(tag_list)
        
        timestamp = int(time.time())
        image_url = f"https://loremflickr.com/800/400/{tags}?random={timestamp}"
        
        print(f"Image URL for '{tags}': {image_url}")
        return image_url
    except Exception as e:
        print(f"Error generating image URL: {e}")
        return f"https://picsum.photos/800/400?random=default"
