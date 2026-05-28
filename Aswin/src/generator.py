# src/generator.py
class GroundedProductDescGenerator:
    def __init__(self, ollama_client):
        self.ollama = ollama_client

    def generate_description(self, product_metadata, retrieved_reviews_context):
        """
        Synthesizes a RAG-grounded product description using Chain-of-Thought (CoT) prompting.
        """
        system_prompt = "You are an expert e-commerce copywriter. You synthesize highly professional, factual, and persuasive product descriptions grounded strictly in product metadata and buyer reviews."
        
        prompt = f"""
        Generate a compelling, detailed product description for the e-commerce storefront based on the provided metadata and verified buyer reviews.
        You MUST follow a Chain-of-Thought (CoT) reasoning approach.

        ### Part 1: Chain-of-Thought Analysis (Solve these steps silently first):
        1. Identify the core product specs, category, and pricing.
        2. Identify the top 3 strengths praised by buyers in the reviews.
        3. Identify any major complaints or criticisms (e.g. cable length, noise) and rephrase them constructively (e.g. "designed for close proximity charging", "robust motor feel").
        4. Synthesize these inputs into a premium, beautifully written 3-paragraph product description.

        ### Input Data:
        Product ID: {product_metadata.get('product_id')}
        Product Name: {product_metadata.get('name')}
        Category: {product_metadata.get('category')}
        Price: ${product_metadata.get('price')}
        Original Specifications: {product_metadata.get('description')}

        Verified Buyer Reviews:
        {retrieved_reviews_context}

        ### Few-Shot Example Output Format:
        **[Product Name] - Reimagined for E-Commerce Excellence**
        *Overview:* [Engaging 2-sentence marketing introduction based on specs]*
        
        *Key Highlights:*
        - **[Feature 1]:** [Grounded detail from reviews]*
        - **[Feature 2]:** [Grounded detail from reviews]*
        - **[Constructive note]:** [Addresses user complaint constructively]*
        
        *Why Customers Love It:*
        [A persuasive closing paragraph summarizing general customer consensus]*

        Now, generate the final grounded product description:
        """
        
        try:
            response = self.ollama.generate(prompt, model_name="gemma2:2b", system_prompt=system_prompt, temperature=0.7)
            return response
        except Exception as e:
            return f"Failed to generate grounded description: {str(e)}"
