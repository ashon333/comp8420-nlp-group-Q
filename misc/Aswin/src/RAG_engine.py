# src/RAG_engine.py
import json
import sqlite3

class RAGEngine:
    def __init__(self, db_path="GroupID_Assignment3/Codes/data/ecommerce_rag.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """
        Creates SQLite tables for products and reviews if they do not exist.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                price REAL,
                description TEXT
            )
        """)
        
        # 2. Reviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id TEXT PRIMARY KEY,
                product_id TEXT,
                username TEXT,
                rating INTEGER,
                text TEXT,
                timestamp INTEGER,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        
        conn.commit()
        conn.close()

    def populate_database(self, products_json_path):
        """
        Loads products and reviews from the JSON dataset and populates the SQLite database.
        """
        try:
            with open(products_json_path, "r") as f:
                products = json.load(f)
        except Exception as e:
            print(f"Failed to open product JSON. Error: {str(e)}")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for prod in products:
            # Insert product
            cursor.execute("""
                INSERT OR REPLACE INTO products (product_id, name, category, price, description)
                VALUES (?, ?, ?, ?, ?)
            """, (prod["product_id"], prod["name"], prod["category"], prod["price"], prod["description"]))
            
            # Insert reviews
            for rev in prod.get("reviews", []):
                cursor.execute("""
                    INSERT OR REPLACE INTO reviews (review_id, product_id, username, rating, text, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (rev["review_id"], prod["product_id"], rev["username"], rev["rating"], rev["text"], rev["timestamp"]))

        conn.commit()
        conn.close()
        print("Database populated successfully from JSON!")

    def add_review(self, product_id, username, rating, text, timestamp):
        """
        Allows inserting a new review dynamically via the Streamlit UI.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Generate new review ID
        cursor.execute("SELECT COUNT(*) FROM reviews")
        count = cursor.fetchone()[0]
        review_id = f"R_NEW_{count + 1}"
        
        cursor.execute("""
            INSERT INTO reviews (review_id, product_id, username, rating, text, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (review_id, product_id, username, rating, text, timestamp))
        
        conn.commit()
        conn.close()
        return review_id

    def get_product(self, product_id):
        """
        Fetches a product's metadata.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_all_products(self):
        """
        Fetches all products.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_product_reviews(self, product_id):
        """
        Fetches all reviews for a specific product.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM reviews WHERE product_id = ?", (product_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def retrieve_context_for_rag(self, product_id, query_search_engine=None, query=None, limit=3):
        """
        Extracts relevant reviews to inject into the RAG prompt context.
        If a search engine is provided, ranks reviews by semantic similarity to the query.
        Otherwise, returns the latest/top reviews.
        """
        reviews = self.get_product_reviews(product_id)
        if not reviews:
            return ""

        context_reviews = []
        if query_search_engine and query:
            # We instantiate a local temporary search engine specifically for context reviews to avoid corrupting global product metadata indexes
            from src.semantic_search import SemanticSearchEngine
            temp_engine = SemanticSearchEngine()
            temp_engine.index_corpus(reviews, text_key="text")
            matches = temp_engine.search(query, top_k=limit)
            context_reviews = [match["item"] for match in matches]
        else:
            # Baseline: top rated or latest
            context_reviews = sorted(reviews, key=lambda r: r["rating"], reverse=True)[:limit]

        context_string = ""
        for i, rev in enumerate(context_reviews):
            user = rev["username"] if rev["username"] else "Anonymous"
            context_string += f"Review #{i+1} by {user} (Rating: {rev['rating']}/5 stars):\n"
            context_string += f"\"{rev['text']}\"\n\n"
            
        return context_string
