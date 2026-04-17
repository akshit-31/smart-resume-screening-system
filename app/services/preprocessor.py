import re
import string

# Try to use NLTK, fallback to basic processing if not available
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer

    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt_tab', quiet=True)

    STOP_WORDS = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    USE_NLTK = True
except Exception:
    USE_NLTK = False
    STOP_WORDS = set()


def preprocess_text(text: str) -> str:
    """Clean and tokenize text for NLP processing."""
    # Lowercase
    text = text.lower()

    # Remove special characters and digits
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    if USE_NLTK:
        tokens = word_tokenize(text)
        tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in STOP_WORDS and len(t) > 2]
    else:
        tokens = [w for w in text.split() if w not in STOP_WORDS and len(w) > 2]

    return ' '.join(tokens)
