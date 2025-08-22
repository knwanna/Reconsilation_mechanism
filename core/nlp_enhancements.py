# core/nlp_enhancements.py
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_lg")

class NLPExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def enhance_query(self, query: str) -> dict:
        doc = nlp(query)
        return {
            "lemmas": [token.lemma_ for token in doc],
            "entities": [(ent.text, ent.label_) for ent in doc.ents],
            "tfidf_vector": self.vectorizer.fit_transform([query])
        }

# Update reconciliation.py
def reconcile(query: str):
    nlp_data = NLPExtractor().enhance_query(query)
    # Use entities for better filtering
    # Use lemmas for expanded search
    # Use TF-IDF for improved scoring