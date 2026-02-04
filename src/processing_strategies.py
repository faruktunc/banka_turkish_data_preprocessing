
from src.stemmer import stem_word
from src.lemmatizer import lemmatize_word

# Strategy 1: Stemming Only (Snowball)
def apply_stemming(tokens):
    """Sadece Snowball Stemmer kullanır."""
    return [stem_word(t) for t in tokens]

# Strategy 2: Lemmatization Only (Zeyrek)
def apply_lemmatization(tokens):
    """Sadece Zeyrek Lemmatizer kullanır (Bulamazsa None döner, biz burada originali koruyacağız)."""
    results = []
    for t in tokens:
        lemma = lemmatize_word(t)
        # Eğer lemma None ise (Unk dahil filtrelendi), orijinali kullan.
        results.append(lemma if lemma else t)
    return results

# Strategy 3: Hybrid (Zeyrek + Backoff to Snowball)
def apply_hybrid(tokens):
    """Zeyrek ile dene, olmazsa Snowball kullan."""
    results = []
    for t in tokens:
        lemma = lemmatize_word(t)
        if lemma:
            results.append(lemma)
        else:
            # Back-off to stemming
            results.append(stem_word(t))
    return results
