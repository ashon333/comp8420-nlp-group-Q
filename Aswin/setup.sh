#!/bin/bash
# automated setup script for E-Commerce Intelligent System

echo "======= Starting IntelliShop AI Environment Setup ======="

# 1. Create virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "--> Creating virtual environment 'env'..."
    python3 -m venv env
else
    echo "--> Virtual environment 'env' already exists."
fi

# 2. Activate virtual environment
echo "--> Activating environment..."
source env/bin/activate

# 3. Upgrade pip
echo "--> Upgrading pip..."
pip install --upgrade pip

# 4. Install dependencies
echo "--> Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# 5. Download spaCy model
echo "--> Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# 6. Download NLTK resources
echo "--> Downloading NLTK tokenizer and lemmatizer corpora..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"

# 7. Check Ollama models
echo "--> Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "Ollama is installed!"
    echo "Checking local models..."
    ollama list
    
    echo "Ensuring required models are available..."
    # We check if gemma2:2b is installed
    if ! ollama list | grep -q "gemma2:2b"; then
        echo "--> Model 'gemma2:2b' not found. Pulling gemma2:2b..."
        ollama pull gemma2:2b
    else
        echo "--> Model 'gemma2:2b' is already available."
    fi
    
    # We check if llama3.2 is installed
    if ! ollama list | grep -q "llama3.2"; then
        echo "--> Model 'llama3.2' not found. Pulling llama3.2..."
        ollama pull llama3.2
    else
        echo "--> Model 'llama3.2' is already available."
    fi
else
    echo "⚠️ Warning: Ollama is not installed or not in PATH. Please run Ollama manually."
fi

echo "======= Environment Setup Completed Successfully! ======="
echo "To activate the environment, run: source env/bin/activate"
echo "To launch the app, run: streamlit run run_dashboard.py"
