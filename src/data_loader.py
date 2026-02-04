import os
import pandas as pd
from config import DATA_DIR, ENCODING, REQUIRED_COLUMNS, BANK_NAME_MAP


def load_bank_csv(filename):
    """Tek banka CSV dosyasını yükler ve temel temizliği yapar."""
    filepath = os.path.join(DATA_DIR, filename)
    df = pd.read_csv(filepath, encoding=ENCODING)

    # Gerekli sütunları seç (mevcut olanlar)
    cols_to_keep = [c for c in REQUIRED_COLUMNS if c in df.columns]
    df = df[cols_to_keep].copy()

    # Banka ismini ekle
    bank_name = BANK_NAME_MAP.get(filename, filename.replace("_reviews.csv", ""))
    df["bank_name"] = bank_name

    # content boş olan satırları düşür
    df = df.dropna(subset=["content"])
    df = df[df["content"].astype(str).str.strip() != ""]
    df = df.reset_index(drop=True)

    # replyContent NaN olanları boş string yap
    if "replyContent" in df.columns:
        df["replyContent"] = df["replyContent"].fillna("")
    else:
        df["replyContent"] = ""

    # score'u int'e çevir
    df["score"] = df["score"].astype(int)

    # thumbsUpCount NaN → 0
    if "thumbsUpCount" in df.columns:
        df["thumbsUpCount"] = df["thumbsUpCount"].fillna(0).astype(int)

    # reviewCreatedVersion, appVersion NaN → boş string
    for col in ["reviewCreatedVersion", "appVersion"]:
        if col in df.columns:
            df[col] = df[col].fillna("")

    # at sütununu datetime'a çevir ve yıl/ay/gün özelliklerini çıkar
    if "at" in df.columns:
        df["at"] = pd.to_datetime(df["at"], errors="coerce")
        df["review_year"] = df["at"].dt.year.astype("Int64")
        df["review_month"] = df["at"].dt.month.astype("Int64")
        df["review_day"] = df["at"].dt.day.astype("Int64")
    else:
        df["review_year"] = pd.NA
        df["review_month"] = pd.NA
        df["review_day"] = pd.NA

    return df


def list_bank_files():
    """Veri klasöründeki tüm CSV dosyalarını listeler."""
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    return sorted(files)


def combine_processed_csvs(output_dir, output_filename="combined_processed.csv"):
    """Output klasöründeki tüm banka CSV'lerini tek dosyada birleştirir."""
    all_dfs = []
    for f in sorted(os.listdir(output_dir)):
        if f.endswith("_processed.csv") and f != output_filename:
            filepath = os.path.join(output_dir, f)
            df = pd.read_csv(filepath)
            all_dfs.append(df)

    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        combined.to_csv(
            os.path.join(output_dir, output_filename), index=False
        )
        return combined
    return pd.DataFrame()
