import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "bankauygulamayorumlar")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
STOPWORDS_FILE = os.path.join(BASE_DIR, "data", "turkish_stopwords.txt")

ENCODING = "utf-8-sig"
MIN_TOKEN_LENGTH = 2
MAX_REPEAT_CHARS = 2

REQUIRED_COLUMNS = ["content", "score", "replyContent", "thumbsUpCount", "at", "reviewCreatedVersion", "appVersion"]

BANK_NAME_MAP = {
    "com.akbank.android.apps.akbank_direkt_reviews.csv": "Akbank",
    "com.denizbank.mobildeniz_reviews.csv": "Denizbank",
    "com.finansbank.mobile.cepsube_reviews.csv": "QNB Finansbank",
    "com.garanti.cepsubesi_reviews.csv": "Garanti BBVA",
    "com.ingbanktr.ingmobil_reviews.csv": "ING Bank",
    "com.kuveytturk.mobil_reviews.csv": "Kuveyt Türk",
    "com.pozitron.iscep_reviews.csv": "İş Bankası",
    "com.teb_reviews.csv": "TEB",
    "com.tfkb_reviews.csv": "Türkiye Finans",
    "com.tmobtech.halkbank_reviews.csv": "Halkbank",
    "com.vakifbank.mobile_reviews.csv": "VakıfBank",
    "com.ykb.android_reviews.csv": "Yapı Kredi",
    "com.ziraat.ziraatmobil_reviews.csv": "Ziraat Bankası",
    "finansbank.enpara_reviews.csv": "Enpara",
}
