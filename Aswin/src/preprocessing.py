# src/preprocessing.py
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Robust corpus check
def ensure_nltk_downloaded():
    # We download 'punkt_tab' alongside other corpora to support newer NLTK word_tokenize runs.
    for resource in ['punkt', 'stopwords', 'wordnet', 'omw-1.4', 'punkt_tab']:
        try:
            if resource == 'punkt':
                nltk.data.find("tokenizers/punkt")
            elif resource == 'punkt_tab':
                nltk.data.find("tokenizers/punkt_tab")
            else:
                nltk.data.find(f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)

ensure_nltk_downloaded()

class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words("english"))
        except Exception:
            self.stop_words = set()

    def normalize(self, text):
        """
        Cleans text by removing HTML tags, punctuation, special characters, and converting to lowercase.
        """
        if not text:
            return ""
        # Remove HTML
        text = re.sub(r"<[^>]+>", " ", text)
        # Convert to lowercase
        text = text.lower()
        # Remove non-alphabetic/numeric characters (keep spaces)
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        # Replace multiple spaces with a single space
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text):
        """
        Splits clean normalized text into words.
        """
        if not text:
            return []
        return word_tokenize(text)

    def remove_stopwords(self, tokens):
        """
        Removes stopwords from a list of tokens.
        """
        return [token for token in tokens if token not in self.stop_words]

    def lemmatize(self, tokens):
        """
        Applies WordNet Lemmatization on a list of tokens.
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]

    def process_pipeline(self, text):
        """
        Full pipeline: Normalize -> Tokenize -> Remove Stopwords -> Lemmatize
        """
        normalized_text = self.normalize(text)
        tokens = self.tokenize(normalized_text)
        clean_tokens = self.remove_stopwords(tokens)
        lemmatized_tokens = self.lemmatize(clean_tokens)
        return {
            "normalized": normalized_text,
            "tokens": tokens,
            "clean_tokens": clean_tokens,
            "lemmatized": lemmatized_tokens,
            "processed_text": " ".join(lemmatized_tokens)
        }
