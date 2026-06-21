# src/extraction.py
import re
import spacy

class InfoExtractor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.has_spacy = True
        except Exception:
            # Fallback if spaCy model is not downloaded
            self.nlp = None
            self.has_spacy = False

    def extract_pos_and_aspects(self, text):
        """
        Uses spaCy's Part-of-Speech (POS) tags to extract nouns (aspects) 
        and adjectives (opinions) from the text.
        """
        aspect_opinion_pairs = []
        nouns = []
        adjectives = []

        if self.has_spacy and self.nlp:
            doc = self.nlp(text)
            # Find Aspect-Opinion relations
            for token in doc:
                if token.pos_ in ["NOUN", "PROPN"]:
                    nouns.append(token.text.lower())
                    # Look for adjectives modifying this noun
                    for child in token.children:
                        if child.pos_ == "ADJ":
                            aspect_opinion_pairs.append({
                                "aspect": token.text.lower(),
                                "opinion": child.text.lower()
                            })
                elif token.pos_ == "ADJ":
                    adjectives.append(token.text.lower())
        else:
            # Simple fallback using naive regex keyword matching
            words = text.lower().split()
            # Mark simple words ending in 'y', 'ful', 'ent', 'ive' as adjectives, others as nouns
            for i, word in enumerate(words):
                if re.match(r"\w+(ful|ent|ive|ous|ble|ing|ed)$", word):
                    adjectives.append(word)
                    if i > 0:
                        nouns.append(words[i-1])
                        aspect_opinion_pairs.append({
                            "aspect": words[i-1],
                            "opinion": word
                        })
                else:
                    if len(word) > 2:
                        nouns.append(word)

        return {
            "nouns": list(set(nouns)),
            "adjectives": list(set(adjectives)),
            "aspect_pairs": aspect_opinion_pairs
        }

    def extract_named_entities(self, text):
        """
        Uses spaCy NER to extract Brands, Locations, and Product Specifications from text.
        """
        entities = []
        if self.has_spacy and self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_
                })
        return entities

    def extract_prices_and_versions(self, text):
        """
        Uses Rule-based Information Extraction (Regex) to pull price tags 
        and technical versions (e.g. UV-C, USB-C, 15-bar, 30-hour).
        """
        # Price extraction: looks for $, optional numbers, dots
        prices = re.findall(r"\$\d+(?:\.\d{2})?", text)
        
        # Version/Spec extraction: e.g., 15-bar, USB-C, 30-hour, P101, etc.
        specs = re.findall(r"\b\d+-(?:bar|hour|day|meter)\b|\b(?:usb-c|uv-c|gps|wi-fi)\b", text, re.IGNORECASE)
        
        return {
            "extracted_prices": list(set(prices)),
            "extracted_specs": list(set(spec.lower() for spec in specs))
        }

    def process_all(self, text):
        """
        Runs aspect-opinion extraction, NER, and Regex specs.
        """
        pos_aspects = self.extract_pos_and_aspects(text)
        entities = self.extract_named_entities(text)
        regex_info = self.extract_prices_and_versions(text)
        
        return {
            "nouns": pos_aspects["nouns"],
            "adjectives": pos_aspects["adjectives"],
            "aspect_pairs": pos_aspects["aspect_pairs"],
            "entities": entities,
            "prices": regex_info["extracted_prices"],
            "specs": regex_info["extracted_specs"]
        }
