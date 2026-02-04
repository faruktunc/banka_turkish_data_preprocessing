import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def prepare_features(df):
    """Etiket kodlama ve ek özellikler ekler."""
    result = df.copy()

    # Score kodlama (1-5 → 0-4)
    le = LabelEncoder()
    result["score_encoded"] = le.fit_transform(result["score"])

    # has_reply özelliği
    result["has_reply"] = result["replyContent"].astype(str).str.strip() != ""

    return result


def select_output_columns(df):
    """Çıktı için gerekli sütunları seçer."""
    columns = [
        # Content variants
        "processed_content_raw_cleaned",
        "processed_content_stemmed",
        "processed_content_lemmatized",
        "processed_content_hybrid",
        # Reply variants
        "processed_reply_raw_cleaned",
        "processed_reply_stemmed",
        "processed_reply_lemmatized",
        "processed_reply_hybrid",
        # Metada + Scores
        "score",
        "score_encoded",
        "has_reply",
        "thumbsUpCount",
        "review_year",
        "review_month",
        "review_day",
        "reviewCreatedVersion",
        "appVersion",
        "bank_name",
    ]
    return df[[c for c in columns if c in df.columns]]


def save_bank_output(df, bank_name, output_dir):
    """Tek banka çıktısını CSV olarak kaydeder."""
    safe_name = (
        bank_name.lower()
        .replace(" ", "_")
        .replace("ı", "i")
        .replace("ö", "o")
        .replace("ü", "u")
        .replace("ş", "s")
        .replace("ç", "c")
        .replace("ğ", "g")
    )
    filename = f"{safe_name}_processed.csv"
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    return filepath
