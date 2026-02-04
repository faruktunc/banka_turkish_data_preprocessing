#!/usr/bin/env python3
"""
Türkçe Banka Yorumları NLP Ön İşleme Pipeline'ı

Her banka CSV dosyasını ayrı ayrı işler, sonra birleştirilmiş çıktı üretir.
"""

import os
import sys
import time

import pandas as pd
from config import DATA_DIR, ENCODING, OUTPUT_DIR
from src.data_loader import load_bank_csv, list_bank_files, combine_processed_csvs
from src.preprocessor import preprocess_dataframe
from src.feature_preparer import prepare_features, select_output_columns, save_bank_output


def process_single_bank(filename):
    """Tek banka dosyasını baştan sona işler."""
    print(f"\n{'='*60}")
    print(f"Banka: {filename}")
    print(f"{'='*60}")

    # 0. Ham CSV üzerinde eksik veri analizi
    raw_path = os.path.join(DATA_DIR, filename)
    raw_df = pd.read_csv(raw_path, encoding=ENCODING)
    print(f"\n  --- Eksik Veri Raporu (Ham CSV) ---")
    print(f"  Toplam satır: {len(raw_df)}")
    for col in raw_df.columns:
        nan_count = raw_df[col].isna().sum()
        if nan_count > 0:
            pct = nan_count / len(raw_df) * 100
            print(f"    {col}: {nan_count} eksik ({pct:.1f}%)")
    non_null_rows = raw_df.dropna(how="all").shape[0]
    print(f"  Tamamen boş olmayan satır: {non_null_rows}")
    print(f"  {'─'*40}")
    del raw_df

    # 1. Veri yükle
    print("  Veri yükleniyor...")
    df = load_bank_csv(filename)
    bank_name = df["bank_name"].iloc[0]
    print(f"  Banka: {bank_name} | Satır sayısı: {len(df)}")

    # Sınıf dağılımı raporu
    print(f"\n  --- Sınıf Dağılımı (score) ---")
    score_counts = df["score"].value_counts().sort_index()
    total = len(df)
    for score_val, count in score_counts.items():
        pct = count / total * 100
        print(f"    Puan {score_val}: {count:>8,} ({pct:5.1f}%)")
    print(f"  {'─'*40}")

    # 2. Ön işleme
    df = preprocess_dataframe(df)

    # 3. Özellik hazırlama
    df = prepare_features(df)

    # 4. Çıktı sütunlarını seç
    df_out = select_output_columns(df)

    # 5. Kaydet
    filepath = save_bank_output(df_out, bank_name, OUTPUT_DIR)
    print(f"  Kaydedildi: {filepath}")

    return bank_name, len(df_out)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    bank_files = list_bank_files()
    print(f"Toplam {len(bank_files)} banka dosyası bulundu.\n")

    start_time = time.time()
    results = []

    for i, filename in enumerate(bank_files, 1):
        print(f"\n[{i}/{len(bank_files)}]", end="")
        bank_name, row_count = process_single_bank(filename)
        results.append((bank_name, row_count))

    # Tüm çıktıları birleştir
    print(f"\n{'='*60}")
    print("Tüm bankalar birleştiriliyor...")
    combined = combine_processed_csvs(OUTPUT_DIR)
    print(f"Birleştirilmiş dosya: output/combined_processed.csv ({len(combined)} satır)")

    # Birleştirilmiş veri seti sınıf dağılımı
    if "score" in combined.columns and len(combined) > 0:
        print(f"\n  --- Genel Sınıf Dağılımı (Tüm Bankalar) ---")
        score_counts = combined["score"].value_counts().sort_index()
        total = len(combined)
        for score_val, count in score_counts.items():
            pct = count / total * 100
            print(f"    Puan {score_val}: {count:>8,} ({pct:5.1f}%)")
        print(f"  {'─'*40}")

    # Özet
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print("ÖZET")
    print(f"{'='*60}")
    for bank_name, count in results:
        print(f"  {bank_name:<25} {count:>8,} satır")
    print(f"  {'─'*40}")
    print(f"  {'TOPLAM':<25} {sum(r[1] for r in results):>8,} satır")
    print(f"\nToplam süre: {elapsed:.1f} saniye")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
