import pandas as pd
from tqdm import tqdm

from src.text_cleaner import clean_text
from src.tokenizer import tokenize
from src.stopword_remover import remove_stopwords
from src.processing_strategies import apply_stemming, apply_lemmatization, apply_hybrid


def preprocess_text(text):
    """Tek bir metne tüm ön işleme adımlarını uygular ve tüm varyasyonları döndürür."""
    # 1. Metin temizleme
    cleaned = clean_text(text)
    if not cleaned:
        return None

    # 2. Tokenization
    tokens = tokenize(cleaned)
    if not tokens:
        return None

    # 3. Stop-word kaldırma (1. geçiş)
    tokens = remove_stopwords(tokens)
    if not tokens:
        return None

    # Varyasyonları Hazırla
    # A. Raw Cleaned (Sadece temizlenmiş + stopword atılmış)
    raw_cleaned = " ".join(tokens)

    # B. Stemmed Only (Snowball)
    stemmed_tokens = apply_stemming(tokens)
    stemmed_tokens = remove_stopwords(stemmed_tokens) # 2. geçiş
    stemmed = " ".join(stemmed_tokens)

    # C. Lemmatized Only (Zeyrek)
    lemma_tokens = apply_lemmatization(tokens)
    lemma_tokens = remove_stopwords(lemma_tokens) # 2. geçiş
    lemmatized = " ".join(lemma_tokens)

    # D. Hybrid (Zeyrek + Backoff) -> Mevcut Yöntem
    hybrid_tokens = apply_hybrid(tokens)
    hybrid_tokens = remove_stopwords(hybrid_tokens) # 2. geçiş
    hybrid = " ".join(hybrid_tokens)

    return {
        "raw_cleaned": raw_cleaned,
        "stemmed": stemmed,
        "lemmatized": lemmatized,
        "hybrid": hybrid
    }


def preprocess_column(series, column_name="content", prefix="content"):
    """Bir pandas Series'e ön işleme uygular ve DataFrame döndürür."""
    tqdm.pandas(desc=f"  {column_name} işleniyor")
    
    # Her satır için dict döner
    results = series.astype(str).progress_apply(preprocess_text)
    
    # Dict'leri DataFrame sütunlarına çevir
    # None olanları boş string yap
    def unpack(d, key):
        if d and isinstance(d, dict):
            return d.get(key, "")
        return ""

    df_result = pd.DataFrame(index=series.index)
    df_result[f"{prefix}_raw_cleaned"] = results.apply(lambda x: unpack(x, "raw_cleaned"))
    df_result[f"{prefix}_stemmed"] = results.apply(lambda x: unpack(x, "stemmed"))
    df_result[f"{prefix}_lemmatized"] = results.apply(lambda x: unpack(x, "lemmatized"))
    df_result[f"{prefix}_hybrid"] = results.apply(lambda x: unpack(x, "hybrid"))
    
    return df_result


def preprocess_dataframe(df):
    """DataFrame'e content ve replyContent ön işlemesi uygular."""
    result = df.copy()

    # Content işle
    print(f"  content sütunu işleniyor ({len(df)} satır)...")
    df_content = preprocess_column(result["content"], "content", "processed_content")
    
    # Yeni sütunları ekle
    for col in df_content.columns:
        result[col] = df_content[col]

    # ReplyContent işle
    print(f"  replyContent sütunu işleniyor...")
    df_reply = preprocess_column(result["replyContent"], "replyContent", "processed_reply")
    
    # Yeni sütunları ekle
    for col in df_reply.columns:
        result[col] = df_reply[col]
        
    # Ön işleme sonrası boş satırları sil
    before_count = len(result)
    empty_mask = result["processed_content_raw_cleaned"].astype(str).str.strip() == ""
    result = result[~empty_mask].reset_index(drop=True)
    dropped_count = before_count - len(result)
    if dropped_count > 0:
        print(f"  Boş satır silindi: {dropped_count} satır (ön işleme sonrası content boş)")

    return result
