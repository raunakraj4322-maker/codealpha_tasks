import re
import string
from typing import List
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class NLPProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self._download_nltk_data()

    def _download_nltk_data(self):
        required_packages = ['punkt', 'punkt_tab', 'stopwords', 'wordnet']
        for package in required_packages:
            try:
                if package in ['punkt', 'punkt_tab']:
                    nltk.data.find(f'tokenizers/{package}')
                else:
                    nltk.data.find(f'corpora/{package}')
            except LookupError:
                try:
                    nltk.download(package, quiet=True)
                except Exception as e:
                    print(f"Warning: Failed to download NLTK package '{package}': {e}")

    def preprocess_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        
        text = text.lower()
        
        text = re.sub(r'[^\w\s]', '', text)
        
        text = re.sub(r'\d+', '', text)
        
        text = text.strip()
        
        tokens = word_tokenize(text)
        
        tokens = [token for token in tokens if token not in self.stop_words]
        
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        processed_text = ' '.join(tokens)
        
        return processed_text

    def preprocess_batch(self, texts: List[str]) -> List[str]:
        return [self.preprocess_text(text) for text in texts]

    def clean_input(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        
        text = text.strip()
        
        text = re.sub(r'\s+', ' ', text)
        
        return text
