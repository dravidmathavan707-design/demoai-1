def is_safe(text):
    # Simple safety check - block certain keywords
    forbidden = ["hack", "exploit", "malware", "virus"]
    text_lower = text.lower()
    for word in forbidden:
        if word in text_lower:
            return False
    return True
