# Turkish Bank App Reviews Data Preprocessing

Bu proje, bankacılık uygulamalarına ait kullanıcı yorumlarını Doğal Dil İşleme (NLP) ve Makine Öğrenmesi (Sentiment Analysis vb.) modelleri için hazırlayan gelişmiş bir ön işleme hattıdır.

## Kurulum (Linux)

Proje **Python 3.8+** gerektirir. Kurulum için aşağıdaki adımları terminalinizde sırasıyla uygulayın:

1. **Virtual Environment (Sanal Ortam) Oluşturun:**
   ```bash
   python3 -m venv venv
   ```

2. **Sanal Ortamı Aktif Edin:**
   ```bash
   source venv/bin/activate
   ```

3. **Gerekli Kütüphaneleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

## Çalıştırma

Pipeline'ı çalıştırarak tüm banka verilerini işlemek için:

```bash
# Sanal ortam aktifken:
python3 pipeline.py

# Veya direkt yol belirterek:
./venv/bin/python3 pipeline.py
```

Bu komut `bankauygulamayorumlar` klasöründeki tüm CSV dosyalarını okuyup işleyecek ve `output` klasörüne kaydedecektir.

Örnek bir çalıştırma çıktısı için [terminal.md](terminal.md) dosyasına bakabilirsiniz.

---

## Örnek Çıktı

Pipeline, yorumları 4 farklı varyasyonla işleyerek zengin bir veri seti sunar.

**Örnek Veri Satırı (Türkiye Finans):**

Bu veriler direkt olarak çıkış dosyasından (`output/turkiye_finans_processed.csv`) alınmıştır.

| Sütun Başlığı | Satır Verisi |
|---|---|
| `processed_content_raw_cleaned` | nfc desteği olan cihaz kullanıyorum nfc desteği olan cihazla kullan diyor |
| `processed_content_stemmed` | nfc destek ola cihaz kullanıyor nfc destek ola cihaz kulla diyor |
| `processed_content_lemmatized` | nfc destek olmak cihaz kullanmak nfc destek olmak cihaz kullanmak demek |
| `processed_content_hybrid` | nfc destek olmak cihaz kullanmak nfc destek olmak cihaz kullanmak demek |
| `processed_reply_raw_cleaned` | yardımcı olmak isteriz talebinize ilişkin detayları isim soy isim iletişim bilgileriniz birlikte adresinden iletebilir misiniz iyi günler |
| `processed_reply_stemmed` | yardımcı olmak ister talep ilişk detay is soy is iletiş bilgi birlik adre iletebilir mi i gün |
| `processed_reply_lemmatized` | yardımcı olmak istemek talep ilişkin detay isim soymak isim iletişim bilgi birlikte adres iletebilir mis iyi günlemek |
| `processed_reply_hybrid` | yardımcı olmak istemek talep ilişkin detay isim soymak isim iletişim bilgi birlikte adres iletebilir mis iyi günlemek |
| `score` | 5 |
| `score_encoded` | 4 |
| `has_reply` | True |
| `thumbsUpCount` | 0 |
| `review_year` | 2025 |
| `review_month` | 8 |
| `review_day` | 19 |
| `reviewCreatedVersion` | 8.6.5 |
| `appVersion` | 8.6.5 |
| `bank_name` | Türkiye Finans |

---

## Uygulanan Yöntemler

Bu proje, Türkçe metin işlemenin zorluklarına (eklemeli yapı, ASCII karakter sorunları vb.) özel çözümler içerir. Detaylar `uygulanacak_yontemler.md` dosyasında mevcuttur.

### 1. Metin Temizleme
- **Küçük Harfe Çevirme:** `İ` -> `i`, `I` -> `ı` kurallarına uygun olarak yapılır.
- **Deasciification:** ASCII karakterler (`guzel`, `cok`) Türkçe'ye (`güzel`, `çok`) çevrilir. (Önce küçük harfe çevrildiği için büyük harfli `COK` gibi kelimeler de doğru düzeltilir).
- **Temizlik:** Emojiler, URL'ler, E-postalar ve noktalama işaretleri temizlenir.

### 2. Tokenization & Stopwords
- Metin boşluklara göre bölünür.
- **Stop-word Temizliği:** NLTK tabanlı özel bir liste kullanılır. **Önemli:** Duygu analizi için kritik olan `iyi`, `kötü`, `çok`, `hiç`, `değil` gibi kelimeler **SİLİNMEZ**, korunur.

### 3. Kök Bulma Stratejileri (Processing Strategies)
Proje 3 farklı stratejiyi aynı anda uygular ve çıktı olarak verir:
- **Stemming:** Snowball kütüphanesi ile hızlı ama kaba kök bulma.
- **Lemmatization:** Zeyrek kütüphanesi ile morfolojik analiz.
- **Hibrit (Hybrid):** Önce Zeyrek ile kök bulunmaya çalışılır. Eğer kelime bulunamazsa ("Unk") Snowball devreye girer. Bu yöntem "bilinmeyen kelime" (UNK) oranını minimize eder.

### 4. Çıktı
Her banka için ayrı bir CSV ve sonunda tüm bankaların birleştiği `combined_processed.csv` oluşturulur.
