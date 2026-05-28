# src/fraud_detection.py
import re
import json

class AuthenticityFraudEngine:
    def __init__(self, traditional_ml_classifier, ollama_client=None):
        self.ml_classifier = traditional_ml_classifier
        self.ollama = ollama_client

    def calculate_stylometrics(self, text):
        """
        Calculates lexical diversity (Type-Token Ratio) and capitalization ratios 
        to detect repetitive templates and weird patterns.
        """
        if not text:
            return {"lexical_diversity": 0.0, "capitalization_ratio": 0.0, "word_count": 0}
            
        words = re.findall(r"\b\w+\b", text.lower())
        unique_words = set(words)
        
        # Type-Token Ratio (TTR)
        ttr = len(unique_words) / len(words) if len(words) > 0 else 0.0
        
        # Capitalization Ratio (checks for uppercase shouting)
        upper_chars = sum(1 for char in text if char.isupper())
        total_chars = len(text)
        cap_ratio = upper_chars / total_chars if total_chars > 0 else 0.0
        
        return {
            "lexical_diversity": round(ttr, 3),
            "capitalization_ratio": round(cap_ratio, 3),
            "word_count": len(words)
        }

    def detect_sentiment_contradiction(self, review_text, star_rating):
        """
        Detects if the text sentiment strongly contradicts the numerical star rating.
        For example: a 5-star rating with highly negative text sentiment.
        """
        # Get probability of positive sentiment from traditional ML [0, 1]
        probs = self.ml_classifier.predict_proba(review_text)
        positive_prob = probs[1]
        
        # Normalize the numerical rating [1, 5] to scale [0, 1]
        normalized_rating = (star_rating - 1) / 4.0
        
        # Absolute discrepancy
        discrepancy = abs(positive_prob - normalized_rating)
        return round(discrepancy, 3)

    def classify_ai_review_llm(self, review_text):
        """
        Uses few-shot learning on Ollama Llama to classify reviews as AI-written or Human-written.
        """
        if not self.ollama:
            return 0.0  # Fallback if Ollama is not initialized
            
        system_prompt = "You are an expert E-Commerce security analyst specializing in AI-written fake review detection."
        
        prompt = f"""
        Analyze the following e-commerce product review and determine the probability (0.0 to 1.0) that it was written by an AI assistant rather than a genuine human buyer.
        AI reviews are typically overly formal, use repetitive flawless vocabulary, contain zero spelling/grammatical errors, lack personal anecdotes, and sound highly structured.
        Human reviews are conversational, may contain small spelling errors or colloquialisms, and detail specific user context.

        ### Labeled Few-Shot Examples:
        Example 1:
        Text: "This product is an absolute masterpiece of modern engineering. The sleek aesthetics paired with state of the art performance creates an unparalleled experience. Highly recommended!"
        Verdict: 0.95 (AI-written)

        Example 2:
        Text: "It makes ok coffee but is really noisy. The cup slides around on the tray and it rattles a lot. Pretty easy to clean though."
        Verdict: 0.05 (Human-written)

        Example 3:
        Text: "I love it! Highly durable and easy to clean. Best purchase of 2026!"
        Verdict: 0.15 (Human-written)

        ### Review to Analyze:
        Text: "{review_text}"

        Provide your analysis in the exact JSON format below. Do not add any extra text or conversational filler:
        {{
            "ai_probability": <float_between_0.0_and_1.0>,
            "reasoning": "<one_sentence_reason>"
        }}
        """
        
        try:
            response_text = self.ollama.generate(prompt, model_name="llama3.2:latest", system_prompt=system_prompt, temperature=0.1)
            
            # Find the JSON substring
            json_match = re.search(r"\{.*?\}", response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                prob = float(data.get("ai_probability", 0.0))
                return prob
            return 0.20  # Safe default if parsing fails
        except Exception as e:
            print("Failed to run LLM AI verification. Error:", str(e))
            # Fallback heuristic: long, flawless sentences with high adjective count and zero punctuation typos get slightly flagged
            if len(review_text.split()) > 20 and "exemplary" in review_text.lower() or "outstanding" in review_text.lower():
                return 0.75
            return 0.15

    def check_user_burstiness(self, username, current_timestamp, review_history):
        """
        Checks if the same user has submitted multiple reviews within a very short timeframe.
        """
        if not username or not review_history:
            return 0  # No username (flagged elsewhere) or no history

        user_timestamps = [
            rev["timestamp"] 
            for rev in review_history 
            if rev["username"] == username and rev["timestamp"] != current_timestamp
        ]
        
        if not user_timestamps:
            return 0

        # Calculate time diffs between the current timestamp and past timestamps
        time_diffs = [abs(current_timestamp - ts) for ts in user_timestamps]
        min_diff = min(time_diffs)
        
        # If user posted within 60 seconds of another post, flag as bursty!
        if min_diff < 60:
            return 1
        return 0

    def evaluate_fraud_index(self, review, user_history=None, run_llm=False):
        """
        Fuses all indicators into a unified, weighted Fraud Index Score (0% to 100%).
        """
        text = review.get("text", "")
        rating = review.get("rating", 3)
        username = review.get("username", "")
        timestamp = review.get("timestamp", 0)

        # 1. Stylometric Check
        styles = self.calculate_stylometrics(text)
        # Low lexical diversity (TTR < 0.40) in reviews of normal length indicates templated spammers
        low_diversity_flag = 1 if styles["word_count"] > 10 and styles["lexical_diversity"] < 0.45 else 0
        shouting_flag = 1 if styles["capitalization_ratio"] > 0.3 else 0

        # 2. Rating-Sentiment Contradiction Check
        discrepancy = self.detect_sentiment_contradiction(text, rating)
        contradiction_flag = 1 if discrepancy > 0.6 else 0

        # 3. Missing Username Check (anonymity is a common trust risk)
        missing_user_flag = 1 if not username or username.strip() == "" else 0

        # 4. Burstiness Check
        bursty_flag = self.check_user_burstiness(username, timestamp, user_history) if user_history else 0

        # 5. AI-Written probability (only run high-latency LLM during dynamic reviews)
        ai_prob = self.classify_ai_review_llm(text) if run_llm else 0.0

        # Unified Weighted Fraud Index Formula
        # Fuses rules (missing user, burst, repetition) and deep models (rating conflict, LLM AI)
        fraud_score = (
            (low_diversity_flag * 0.15) +
            (shouting_flag * 0.10) +
            (contradiction_flag * 0.25) +
            (missing_user_flag * 0.15) +
            (bursty_flag * 0.15) +
            (ai_prob * 0.20)
        )
        
        fraud_percentage = min(int(fraud_score * 100), 100)
        
        flags = {
            "low_lexical_diversity": bool(low_diversity_flag),
            "excessive_shouting": bool(shouting_flag),
            "sentiment_rating_contradiction": bool(contradiction_flag),
            "anonymous_reviewer": bool(missing_user_flag),
            "burst_posting_rate": bool(bursty_flag)
        }
        
        return {
            "fraud_score": fraud_percentage,
            "stylometrics": styles,
            "sentiment_rating_discrepancy": discrepancy,
            "ai_written_confidence": round(ai_prob * 100, 1),
            "flags": flags
        }
