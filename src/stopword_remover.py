import os
from config import STOPWORDS_FILE


def load_stopwords(filepath):
    """Stop-word dosyasını okur. Yorum satırları (#) ve boş satırlar atlanır."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Stop-word dosyası bulunamadı: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        words = set()
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                words.add(line)
    return words


_STOPWORDS_CACHE = None


def _get_cached_stopwords():
    global _STOPWORDS_CACHE
    if _STOPWORDS_CACHE is None:
        _STOPWORDS_CACHE = load_stopwords(STOPWORDS_FILE)
    return _STOPWORDS_CACHE


def remove_stopwords(tokens):
    """Token listesinden stop-word'leri kaldırır."""
    stopwords = _get_cached_stopwords()
    return [t for t in tokens if t not in stopwords]
