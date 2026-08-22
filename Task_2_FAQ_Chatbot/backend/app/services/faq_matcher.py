import json
from typing import List, Dict, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .nlp_processor import NLPProcessor
from ..config import settings


class FAQMatcher:
    def __init__(self, faq_data_path: str):
        self.nlp_processor = NLPProcessor()
        self.faq_data_path = faq_data_path
        self.faqs: List[Dict] = []
        self.faq_questions: List[str] = []
        self.tfidf_vectorizer: Optional[TfidfVectorizer] = None
        self.faq_vectors: Optional[np.ndarray] = None
        self._load_faqs()
        self._build_vectorizer()

    def _load_faqs(self):
        try:
            with open(self.faq_data_path, 'r', encoding='utf-8') as f:
                self.faqs = json.load(f)
            
            self.faq_questions = [faq['question'] for faq in self.faqs]
            
            for i, faq in enumerate(self.faqs):
                faq['preprocessed_question'] = self.nlp_processor.preprocess_text(faq['question'])
                
        except FileNotFoundError:
            raise FileNotFoundError(f"FAQ data file not found at {self.faq_data_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in FAQ data file at {self.faq_data_path}")

    def _build_vectorizer(self):
        preprocessed_questions = [faq['preprocessed_question'] for faq in self.faqs]
        
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            stop_words='english'
        )
        
        self.faq_vectors = self.tfidf_vectorizer.fit_transform(preprocessed_questions)

    def match_question(self, user_question: str) -> Dict:
        if not user_question or not isinstance(user_question, str):
            return self._get_fallback_response()
        
        cleaned_question = self.nlp_processor.clean_input(user_question)
        
        if not cleaned_question or len(cleaned_question) < 3:
            return self._get_fallback_response()
        
        preprocessed_question = self.nlp_processor.preprocess_text(cleaned_question)
        
        if not preprocessed_question:
            return self._get_fallback_response()
        
        try:
            user_vector = self.tfidf_vectorizer.transform([preprocessed_question])
            
            similarity_scores = cosine_similarity(user_vector, self.faq_vectors)[0]
            
            best_match_idx = np.argmax(similarity_scores)
            best_score = similarity_scores[best_match_idx]
            
            if best_score >= settings.similarity_threshold:
                matched_faq = self.faqs[best_match_idx]
                return {
                    'answer': matched_faq['answer'],
                    'matched_question': matched_faq['question'],
                    'confidence': float(best_score),
                    'category': matched_faq.get('category', 'General'),
                    'faq_id': matched_faq['id']
                }
            else:
                return self._get_fallback_response()
                
        except Exception as e:
            return self._get_fallback_response()

    def _get_fallback_response(self) -> Dict:
        return {
            'answer': "I'm sorry, I couldn't find a sufficiently relevant answer to that question. Please try asking in a different way, or browse our FAQ section for more information.",
            'matched_question': None,
            'confidence': 0.0,
            'category': None,
            'faq_id': None
        }

    def get_all_faqs(self) -> List[Dict]:
        return [{
            'id': faq['id'],
            'question': faq['question'],
            'answer': faq['answer'],
            'category': faq.get('category', 'General')
        } for faq in self.faqs]

    def get_categories(self) -> List[str]:
        categories = set(faq.get('category', 'General') for faq in self.faqs)
        return sorted(list(categories))

    def get_similar_questions(self, query: str, top_k: int = 5) -> List[str]:
        if not query or not isinstance(query, str):
            return []
        
        cleaned_query = self.nlp_processor.clean_input(query)
        preprocessed_query = self.nlp_processor.preprocess_text(cleaned_query)
        
        if not preprocessed_query:
            return []
        
        try:
            query_vector = self.tfidf_vectorizer.transform([preprocessed_query])
            similarity_scores = cosine_similarity(query_vector, self.faq_vectors)[0]
            
            top_indices = np.argsort(similarity_scores)[-top_k:][::-1]
            
            similar_questions = [self.faq_questions[idx] for idx in top_indices if similarity_scores[idx] > 0.1]
            
            return similar_questions[:top_k]
        except Exception:
            return []
