import logging
import zeyrek

# Zeyrek'in "APPENDING RESULT" warning çıktılarını bastır
logging.getLogger("zeyrek").setLevel(logging.ERROR)

_analyzer = None
_cache = {}


def _get_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = zeyrek.MorphAnalyzer()
    return _analyzer


def _pick_best_lemma(parses):
    """Birden fazla analiz sonucundan en uygun lemmayı seçer.

    Heuristik: En uzun lemmayı tercih et (daha fazla kök bilgisi taşır).
    Ör: 'kullanıyorum' → 'kullanmak' (9) vs 'kul' (3) → 'kullanmak' seçilir.
    """
    if not parses:
        return None

    best_lemma = None
    best_len = -1
    for parse in parses:
        lemma = parse.lemma.lower()
        if lemma == "unk":
            continue
        if len(lemma) > best_len:
            best_len = len(lemma)
            best_lemma = lemma
    return best_lemma


def lemmatize_word(word):
    """Tek kelimeyi Zeyrek ile lemmatize eder. Cache kullanır.

    Returns:
        str veya None: Lemma bulunduysa döndürür, bulunamadıysa None.
    """
    if word in _cache:
        return _cache[word]

    analyzer = _get_analyzer()
    try:
        results = analyzer.analyze(word)
        if results and results[0]:
            lemma = _pick_best_lemma(results[0])
            if lemma:
                _cache[word] = lemma
                return lemma
    except Exception:
        pass

    _cache[word] = None
    return None


def lemmatize_tokens(tokens):
    """Token listesini lemmatize eder.

    Returns:
        list[tuple]: (lemma_or_original, was_lemmatized) çiftleri
    """
    results = []
    for token in tokens:
        lemma = lemmatize_word(token)
        if lemma is not None:
            results.append((lemma, True))
        else:
            results.append((token, False))
    return results


def clear_cache():
    """Lemma cache'ini temizler."""
    global _cache
    _cache = {}
