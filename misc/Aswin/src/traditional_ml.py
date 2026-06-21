# src/traditional_ml.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class TraditionalMLClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        self.model = LogisticRegression(C=1.0)
        self.is_trained = False
        
        # Self-contained pre-training corpus to ensure instant functionality
        self._pretrain_baseline()

    def _pretrain_baseline(self):
        """
        Trains the classifier on a standard, high-quality synthesized dataset of e-commerce reviews
        so it works out-of-the-box.
        """
        training_corpus = [
            # Positive Reviews (Label: 1)
            ("Absolutely amazing product! Best purchase I have made in a long time.", 1),
            ("Highly recommend! Excellent build quality and extremely comfortable.", 1),
            ("Exceeded my expectations. Flawless operation and battery lasts forever.", 1),
            ("Very satisfied. Super fast shipping, works perfectly.", 1),
            ("Great design, very premium feel, and outstanding performance.", 1),
            ("This is beautiful and functions incredibly well.", 1),
            ("Love it! Highly durable and easy to clean.", 1),
            ("Crema is rich and espresso tastes fantastic.", 1),
            # Negative Reviews (Label: 0)
            ("Absolute garbage! Ruined my kitchen and started leaking on day two.", 0),
            ("Absolute garbage! Spares broke on day one.", 0),
            ("Terrible quality. Spares broke immediately, do not buy!", 0),
            ("Extremely disappointed. Plastic feels cheap and screen keeps freezing.", 0),
            ("Horrible customer support and app keeps crashing.", 0),
            ("Waste of money. Fails to charge and reservoir leaks everywhere.", 0),
            ("Very noisy, vibrates too much, and feels poorly made.", 0),
            ("Cheap construction, broke after three weeks.", 0),
            ("Leaked from the bottom. Refused to heat up. Horrible.", 0)
        ]
        
        texts = [item[0] for item in training_corpus]
        labels = [item[1] for item in training_corpus]
        
        self.fit(texts, labels)

    def fit(self, texts, labels):
        """
        Trains/fits the TF-IDF Vectorizer and Logistic Regression model on custom reviews.
        """
        X = self.vectorizer.fit_transform(texts)
        y = np.array(labels)
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, text):
        """
        Predicts sentiment category: 0 = Negative, 1 = Positive.
        """
        if not self.is_trained:
            raise ValueError("Traditional ML model is not trained yet.")
        
        X_test = self.vectorizer.transform([text])
        pred = self.model.predict(X_test)[0]
        return int(pred)

    def predict_proba(self, text):
        """
        Returns probability distribution for [Negative, Positive] classes.
        Useful for calculating Sentiment-Rating Discrepancies.
        """
        if not self.is_trained:
            raise ValueError("Traditional ML model is not trained yet.")
        
        X_test = self.vectorizer.transform([text])
        proba = self.model.predict_proba(X_test)[0]
        return proba
