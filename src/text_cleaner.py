import regex

try:
    from turkish.deasciifier import Deasciifier
    _HAS_DEASCIIFIER = True
except ImportError:
    _HAS_DEASCIIFIER = False


def deasciify(text):
    """ASCII Türkçe'yi doğru Türkçe karakterlere çevirir."""
    if not _HAS_DEASCIIFIER:
        return text
    try:
        return Deasciifier(text).convert_to_turkish()
    except Exception:
        return text


def turkish_lower(text):
    """Türkçe'ye özel küçük harfe çevirme."""
    text = text.replace("I", "ı").replace("İ", "i")
    return text.lower()


def remove_emojis(text):
    """Emoji karakterlerini kaldırır (temel ASCII rakam/semboller hariç)."""
    return regex.sub(
        r"[\p{Emoji}--[0-9#*\u00a9\u00ae\u2122]]",
        " ",
        text,
    )


def remove_urls(text):
    """URL'leri kaldırır."""
    text = regex.sub(r"https?://\S+", " ", text)
    text = regex.sub(r"www\.\S+", " ", text)
    return text


def remove_emails(text):
    """E-posta adreslerini kaldırır."""
    return regex.sub(r"\S+@\S+\.\S+", " ", text)


def remove_phone_numbers(text):
    """Türk telefon numaralarını kaldırır."""
    # +90 ile başlayan
    text = regex.sub(r"\+90[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}", " ", text)
    # 0 ile başlayan
    text = regex.sub(r"\b0\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}\b", " ", text)
    # Genel uzun sayı dizileri (10+ hane)
    text = regex.sub(r"\b\d{10,}\b", " ", text)
    return text


def normalize_repeated_chars(text, max_repeat=2):
    """Tekrar eden karakterleri belirli sayıya indirir."""
    pattern = r"(.)\1{" + str(max_repeat) + r",}"
    replacement = r"\1" * max_repeat
    return regex.sub(pattern, replacement, text)


def remove_numbers(text):
    """Bağımsız sayıları kaldırır."""
    return regex.sub(r"\b\d+\b", " ", text)


def remove_punctuation(text):
    """Harf, rakam ve boşluk dışındaki karakterleri kaldırır."""
    return regex.sub(r"[^\p{L}\p{N}\s]", " ", text)


def normalize_whitespace(text):
    """Çoklu boşlukları teke indirir, baş/son boşlukları temizler."""
    return regex.sub(r"\s+", " ", text).strip()


def clean_text(text):
    """Tüm temizleme adımlarını sırasıyla uygular."""
    if not isinstance(text, str) or not text.strip():
        return ""

    text = turkish_lower(text)
    text = deasciify(text)
    
    text = remove_emojis(text)
    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_phone_numbers(text)
    text = normalize_repeated_chars(text)
    text = remove_numbers(text)
    text = remove_punctuation(text)
    text = normalize_whitespace(text)
    return text
