# run_dashboard.py
import time
import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
from src.agent_ensemble import IntellishopEnsembleCoordinator

# 1. Page Configuration
st.set_page_config(
    page_title="IntelliShop AI Storefront Operations",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Dark/Glassmorphic Style Custom CSS (Highly Clean & Professional)
st.markdown("""
<style>
    /* Main Background & Fonts */
    .main {
        background-color: #0c0e17;
        color: #f1f2f6;
        font-family: 'Inter', sans-serif;
    }
    
    /* Title and Header */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
    }
    
    /* Streamlit Cards styling */
    div.stMetric {
        background: rgba(30, 34, 53, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 15px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .premium-card {
        background: rgba(26, 30, 48, 0.55);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        color: #e4e7eb;
    }
    
    .onboarding-card {
        background: linear-gradient(135deg, rgba(108, 92, 231, 0.15) 0%, rgba(30, 34, 53, 0.5) 100%);
        border: 1px solid rgba(108, 92, 231, 0.3);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
    }
    
    /* Buttons Customization */
    .stButton>button {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3) !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.5) !important;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div {
        background-color: #141724 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    /* Metrics numbers and labels */
    div[data-testid="stMetricValue"] {
        color: #818cf8 !important;
        font-weight: bold;
    }
    
    /* Custom Badge/Tag */
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
        display: inline-block;
        margin-right: 5px;
    }
    .badge-success { background-color: rgba(0, 184, 148, 0.2); color: #2ecc71; border: 1px solid #2ecc71; }
    .badge-warning { background-color: rgba(254, 202, 87, 0.2); color: #f1c40f; border: 1px solid #f1c40f; }
    .badge-danger { background-color: rgba(255, 118, 117, 0.2); color: #e74c3c; border: 1px solid #e74c3c; }
    .badge-info { background-color: rgba(116, 185, 255, 0.2); color: #3498db; border: 1px solid #3498db; }
</style>
""", unsafe_allow_html=True)

# 3. Instantiate Central Coordinator
@st.cache_resource
def get_coordinator():
    # Automatically triggers database rebuild on real Amazon reviews dataset
    # Uses db_path relative to Codes/
    return IntellishopEnsembleCoordinator(db_path="data/ecommerce_rag.db", products_json_path="data/products_reviews.json")

try:
    coordinator = get_coordinator()
except Exception as e:
    st.error(f"Failed to load engine components: {str(e)}")
    st.stop()

# 4. Header & Branding Section
st.title("🛍️ IntelliShop: E-Commerce Storefront AI Coprocessor")

# On-boarding Explainer: Explains clearly WHAT the app does!
st.markdown("""
<div class="onboarding-card">
    <h3 style="margin-top:0; color:#818cf8 !important;">💡 What is this application for?</h3>
    <p>This console is designed for e-commerce operators to manage product listings and secure customer reviews using 12 combined basic and advanced Natural Language Processing (NLP) techniques. It solves two critical storefront problems:</p>
    <div style="display: flex; gap: 20px; margin-top: 15px;">
        <div style="flex: 1; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px;">
            <strong style="color: #ff7675;">🛡️ Problem 1: Review Fraud &amp; AI Ingestion</strong><br>
            Automatically screens user-submitted product reviews to flag fake spam, anomalous posting bursts, rating-text contradictions, and AI-written text.
        </div>
        <div style="flex: 1; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px;">
            <strong style="color: #55efc4;">✨ Problem 2: RAG storefront Copywriter</strong><br>
            Instantly generates persuasive, grounded storefront descriptions reading real buyer reviews, verified by a strict independent LLM-as-a-Judge critic.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Sidebar - Simple step-by-step navigation
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <h2 style='color: #818cf8 !important; margin-bottom: 5px;'>🛍️ IntelliShop Console</h2>
    <span style='font-size: 11px; color: #a29bfe; background: rgba(108, 92, 231, 0.2); padding: 3px 8px; border-radius: 10px;'>Official Amazon Reviews Dataset</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("Step 1: Product Discovery")
search_mode = st.sidebar.radio("Discovery Search Mode", ["Browse Categories", "Semantic Search (Natural Language) 🧠"])

query = ""
if search_mode == "Semantic Search (Natural Language) 🧠":
    query = st.sidebar.text_input("Type what you want to do (e.g. 'read books at night' or 'connect smart plug')", placeholder="Search user intent...")
    st.sidebar.caption("💡 Matches products using SentenceTransformer embeddings & Cosine similarity.")
else:
    category_filter = st.sidebar.selectbox("Active Catalog Category", ["All Products", "Electronics", "Smart Home"])

# Product Filtering
if search_mode == "Semantic Search (Natural Language) 🧠" and query:
    search_results = coordinator.dynamic_semantic_search(query, top_k=3)
    filtered_products = [res["item"] for res in search_results if res["score"] > 0.05]
    if not filtered_products:
        st.sidebar.warning("No semantic match found. Showing catalog.")
        filtered_products = coordinator.rag_db.get_all_products()
else:
    all_prods = coordinator.rag_db.get_all_products()
    if search_mode == "Browse Categories" and category_filter != "All Products":
        filtered_products = [p for p in all_prods if p["category"] == category_filter]
    else:
        filtered_products = all_prods

# Clear Dropdown list
product_options = {p["product_id"]: f"{p['name']} (${p['price']})" for p in filtered_products}
if product_options:
    selected_prod_id = st.sidebar.selectbox("Active Storefront Product:", list(product_options.keys()), format_func=lambda x: product_options[x])
else:
    st.sidebar.warning("No matches found. Loading fallback.")
    selected_prod_id = coordinator.rag_db.get_all_products()[0]["product_id"]

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size: 10px; color: #8a8d9a; line-height: 1.4;'>
    <b>Technical Pipeline Status:</b><br>
    ✓ Preprocessing: NLTK Lemmatizer<br>
    ✓ Aspects: spaCy POS Extractor<br>
    ✓ Baseline Sentiment: TF-IDF + Logistic Reg<br>
    ✓ Vectors: local all-MiniLM Cosine Search<br>
    ✓ Generative LLMs: local Gemma2 & Llama3 (Ollama)<br>
    ✓ Grounding Store: SQLite Vector RAG
</div>
""", unsafe_allow_html=True)

# Fetch data for active product
product = coordinator.rag_db.get_product(selected_prod_id)
reviews = coordinator.rag_db.get_product_reviews(selected_prod_id)

# ================= STEP 2: ACTIVE PRODUCT DISPLAY =================
st.markdown("### Step 2: Storefront Catalog Details")
col_p_left, col_p_right = st.columns([1, 2])

with col_p_left:
    st.markdown(f"""
    <div class="premium-card" style="border-left: 4px solid #818cf8; margin-bottom: 10px;">
        <span class="badge badge-info">{product['category']}</span>
        <h2 style="margin-top: 10px; margin-bottom: 5px;">{product['name']}</h2>
        <h3 style="color: #818cf8 !important; margin-top: 0;">${product['price']}</h3>
        <p style="font-size: 13px; color: #a0aec0; font-style: italic; margin-bottom: 0;">Reference specifications: "{product['description']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render the dynamic product image from the Kaggle dataset
    import os
    img_path = f"data/images/{selected_prod_id.lower()}.jpg"
    if os.path.exists(img_path):
        st.image(img_path, caption=product['name'], use_container_width=True)

with col_p_right:
    # Key Stats Metrics
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0.0
    
    # Calculate Risk
    fraud_flags_count = 0
    for r in reviews:
        anal = coordinator.analyze_single_review(r["text"], r["rating"], r["username"], r["timestamp"])
        if anal["fraud_analysis"]["fraud_score"] > 35:
            # Flaggable score threshold
            fraud_flags_count += 1
            
    risk_level = "CRITICAL RISK (SPAM FOUND)" if fraud_flags_count >= 2 else ("WARNING RISK" if fraud_flags_count == 1 else "SECURE (LOW RISK)")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("Total Buyer Reviews", len(reviews))
    with m_col2:
        st.metric("Verified Average Rating", f"{round(avg_rating, 1)} / 5.0")
    with m_col3:
        st.metric("Storefront Review Integrity", risk_level)

# ================= STEP 3: REVIEW SECURITY GUARD PORTAL =================
st.markdown("---")
st.markdown("### Step 3: Review Security Guard (Fraud & Spam Ingestion)")
st.write("Audits and processes customer reviews. Suspicious text, templates, ratings contradictions, or AI signatures are flagged automatically.")

col_rg_left, col_rg_right = st.columns([1, 2])

with col_rg_left:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.write("#### 📊 POS Aspects & Opinion breakdown")
    st.write("Identifies feature-level nouns (Aspects) and adjectives (Opinions) using spaCy POS dependencies:")
    
    # Aggregate aspects
    all_aspects = []
    pos_count = 0
    neg_count = 0
    
    for r in reviews:
        anal = coordinator.analyze_single_review(r["text"], r["rating"], r["username"], r["timestamp"])
        all_aspects.extend(anal["extracted_features"]["aspect_pairs"])
        if anal["traditional_ml"]["sentiment_label"] == "Positive":
            pos_count += 1
        else:
            neg_count += 1
            
    # Chart
    fig_pie = px.pie(
        names=["Positive", "Negative"],
        values=[pos_count, neg_count],
        color=["Positive", "Negative"],
        color_discrete_map={"Positive": "#00b894", "Negative": "#d63031"},
        hole=0.4,
        title="Reviews Polar Sentiment Breakdown"
    )
    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#fff")
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.write("**Extracted Noun Aspects:**")
    if all_aspects:
        df_a = pd.DataFrame(all_aspects).drop_duplicates().head(5)
        st.table(df_a)
    else:
        st.write("No distinct aspects identified yet.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_rg_right:
    st.write("#### 🛡️ Live Reviews Audit Feed")
    
    for rev in reviews:
        # Performance Optimized: skips Llama-inference for simple static lists
        anal = coordinator.analyze_single_review(rev["text"], rev["rating"], rev["username"], rev["timestamp"], run_llm=False)
        fraud_score = anal["fraud_analysis"]["fraud_score"]
        
        # Fraud Indicator tags
        badge_class = "badge-success" if fraud_score < 30 else ("badge-warning" if fraud_score < 60 else "badge-danger")
        badge_text = "SECURE" if fraud_score < 30 else ("SUSPICIOUS" if fraud_score < 60 else "🚨 CRITICAL SPAM ALERT")
        
        user_display = rev["username"] if rev["username"] else "Anonymous Reviewer (FLAGGED)"
        
        st.markdown(f"""
        <div class="premium-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong>👤 {user_display}</strong>
                <span>Rating: {'★' * rev['rating']}{'☆' * (5 - rev['rating'])}</span>
            </div>
            <p style="font-style: italic; color: #e2e8f0; margin-bottom: 10px;">"{rev['text']}"</p>
            <div style="margin-top: 10px; display:flex; gap:10px; align-items:center;">
                <span class="badge {badge_class}">{badge_text} (Score: {fraud_score}%)</span>
                <span style="font-size: 11px; color:#a0aec0;">Extracted Specs: {anal['extracted_features']['specs']}</span>
            </div>
            <hr style="border:0.5px solid rgba(255,255,255,0.05); margin: 12px 0;">
            <details style="font-size: 12px; color: #a29bfe; cursor: pointer;">
                <summary>🔍 View Core NLP & Forensic metrics</summary>
                <div style="background-color: #0c0e17; padding: 12px; border-radius: 8px; margin-top: 8px;">
                    <strong>Lemmatized tokens:</strong> {anal['preprocessed']['lemmatized']}<br>
                    <strong>NER Entities:</strong> {anal['extracted_features']['entities']}<br>
                    <strong>Contradiction score:</strong> Discrepancy = {anal['fraud_analysis']['sentiment_rating_discrepancy']}<br>
                    <strong>Flags:</strong> {anal['fraud_analysis']['flags']}
                </div>
            </details>
        </div>
        """, unsafe_allow_html=True)

# ================= STEP 4: AI PRODUCT GENERATOR & JUDGE =================
st.markdown("---")
st.markdown("### Step 4: RAG-Grounded Copywriter & AI Judge")
st.write("Invokes local Gemma-2B to generate grounded description context and local Llama-3.2 to run independent QA scorecard audits.")

if st.button("✨ Click to Generate Grounded Description"):
    with st.spinner("Retrieving reviews from SQLite and synthesizing copy..."):
        results = coordinator.generate_and_judge_product_description(selected_prod_id, semantic_query=query if query else None)
        
        if "error" in results:
            st.error(results["error"])
        else:
            col_g, col_j = st.columns([1, 1])
            
            with col_g:
                st.success("##### synthesized Copy (Gemma-2B via RAG)")
                st.markdown(f"""
                <div class="premium-card" style="background-color: #121420;">
                    {results['generated_description']}
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("🔍 View Grounding reviews"):
                    st.text(results["retrieved_context"])
                    
            with col_j:
                st.info("##### Independent Critic Scorecard (Llama-as-a-Judge)")
                scorecard = results["scorecard"]
                
                verdict = scorecard.get("overall_audit_verdict", "NEEDS REVISION")
                verdict_color = "#2ecc71" if "APPROVED" in verdict else "#e74c3c"
                
                st.markdown(f"""
                <div class="premium-card" style="background-color: #121420; border: 1.5px solid rgba(129, 140, 248, 0.4);">
                    <h3 style="text-align: center; color: {verdict_color} !important;">Verdict: {verdict}</h3>
                    <hr style="border:0.5px solid rgba(255,255,255,0.05); margin: 12px 0;">
                    <div style="margin-bottom: 10px;">
                        <strong>Factual Consistency: {scorecard.get('factual_consistency', {}).get('score', 0)}/5</strong><br>
                        <span style="font-size:12px; color:#a0aec0;">Reason: {scorecard.get('factual_consistency', {}).get('reasoning', '')}</span>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>Freedom from Hallucinations: {scorecard.get('hallucination_rate', {}).get('score', 0)}/5</strong><br>
                        <span style="font-size:12px; color:#a0aec0;">Reason: {scorecard.get('hallucination_rate', {}).get('reasoning', '')}</span>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>Tonal Professionalism: {scorecard.get('tonal_professionalism', {}).get('score', 0)}/5</strong><br>
                        <span style="font-size:12px; color:#a0aec0;">Reason: {scorecard.get('tonal_professionalism', {}).get('reasoning', '')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ================= STEP 5: REVIEW INGESTION FORM =================
st.markdown("---")
st.markdown("### Step 5: Ingest & Test Custom Reviews")
st.write("Write a review yourself to test the system in real-time! Write an AI review, an anonymous review, or contradictory sentiment text and click submit.")

with st.form("dynamic_review_form"):
    test_username = st.text_input("Reviewer Username:", placeholder="e.g. buyer_jack")
    test_rating = st.slider("Rating (Stars):", 1, 5, 5)
    test_text = st.text_area("Review Content:", placeholder="Type review here...")
    
    submitted = st.form_submit_button("Submit & Audit Ingested Review")
    
    if submitted:
        if not test_text.strip():
            st.error("Please enter valid text.")
        else:
            with st.spinner("Ingesting and running deep AI checks..."):
                current_time = int(time.time())
                
                # Ingest review to SQLite
                new_id = coordinator.rag_db.add_review(
                    product_id=selected_prod_id,
                    username=test_username.strip(),
                    rating=test_rating,
                    text=test_text.strip(),
                    timestamp=current_time
                )
                
                # Run full analysis including LLM checks
                analysis = coordinator.analyze_single_review(
                    test_text.strip(), 
                    test_rating, 
                    test_username.strip(), 
                    current_time, 
                    run_llm=True
                )
                
                fraud_score = analysis["fraud_analysis"]["fraud_score"]
                ai_confidence = analysis["fraud_analysis"]["ai_written_confidence"]
                
                st.success(f"Review Ingested successfully into SQLite! Assigned ID: {new_id}")
                
                st.markdown("<div class='premium-card' style='border: 1px solid rgba(129, 140, 248, 0.4);'>", unsafe_allow_html=True)
                st.write("### 🚨 Forensic Security Audit Results:")
                
                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1:
                    st.metric("Unified Fraud Index Score", f"{fraud_score}%")
                with col_f2:
                    st.metric("AI-Written Probability", f"{ai_confidence}%")
                with col_f3:
                    st.metric("Rating-Sentiment Discrepancy", f"{analysis['fraud_analysis']['sentiment_rating_discrepancy']}")
                
                st.write("#### Extracted NLP Aspects & Tokens:")
                st.json({
                    "tokens_lemmatized": analysis["preprocessed"]["lemmatized"],
                    "aspect_pairs": analysis["extracted_features"]["aspect_pairs"],
                    "named_entities": analysis["extracted_features"]["entities"],
                    "regex_extracted": {
                        "prices": analysis["extracted_features"]["prices"],
                        "specs": analysis["extracted_features"]["specs"]
                    },
                    "active_fraud_alerts": analysis["fraud_analysis"]["flags"]
                })
                st.markdown("</div>", unsafe_allow_html=True)
                st.info("The review has been added. Switch back to Step 3 to see it in the main review stream!")
