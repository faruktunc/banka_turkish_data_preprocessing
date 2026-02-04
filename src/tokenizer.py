from config import MIN_TOKEN_LENGTH


def tokenize(text):
    """Metni boşluklara göre token'lara ayırır, kısa token'ları filtreler."""
    if not text:
        return []
    tokens = text.split()
    return [t for t in tokens if len(t) >= MIN_TOKEN_LENGTH]
