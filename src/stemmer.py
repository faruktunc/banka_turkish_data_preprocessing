import snowballstemmer

_stemmer = snowballstemmer.stemmer("turkish")


def stem_word(word):
    """Tek kelimeyi Snowball TurkishStemmer ile kökler."""
    result = _stemmer.stemWord(word)
    return result if result else word


def lemmatize_with_backoff(tokens):
    """Önce Zeyrek lemmatization, başarısız olursa Snowball stemming.

    Args:
        tokens: Lemmatize edilecek token listesi

    Returns:
        list[str]: Lemma/stem sonuçları
    """
    from src.lemmatizer import lemmatize_tokens

    lemma_results = lemmatize_tokens(tokens)
    final = []
    for lemma_or_orig, was_lemmatized in lemma_results:
        if was_lemmatized:
            final.append(lemma_or_orig)
        else:
            # Zeyrek başarısız → Snowball stemmer'a düş
            stemmed = stem_word(lemma_or_orig)
            final.append(stemmed)
    return final
