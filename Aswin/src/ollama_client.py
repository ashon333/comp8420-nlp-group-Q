# src/ollama_client.py
import json
import requests

class OllamaOrchestrator:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.default_gemma = "gemma2:2b"
        self.default_llama = "llama3.2:latest"
        
        # Verify available models
        self.available_models = self.get_available_models()

    def get_available_models(self):
        """
        Fetches the list of models installed locally in Ollama.
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            if response.status_code == 200:
                models_info = response.json().get("models", [])
                names = [model["name"] for model in models_info]
                print("Available Ollama models:", names)
                return names
            return []
        except Exception:
            print("⚠️ Warning: Could not connect to local Ollama. Make sure Ollama app is running!")
            return []

    def get_best_model(self, preferred_model):
        """
        Determines the best model to use. Fallback if preferred is missing.
        """
        if not self.available_models:
            # Re-try once
            self.available_models = self.get_available_models()
            
        if not self.available_models:
            return preferred_model # Default fallback try
            
        # Check exact or prefix match
        for model in self.available_models:
            if preferred_model in model or model in preferred_model:
                return model
                
        # If preferred model is gemma but not found, look for llama3.2/llama3.1
        if "gemma" in preferred_model:
            for model in ["llama3.2:latest", "llama3.2:3b", "llama3.1:latest", "llama3.1:8b", "llama3.2", "llama3.1"]:
                if model in self.available_models:
                    print(f"Preferred model '{preferred_model}' not found. Falling back to '{model}'")
                    return model
        # Default to first available model if any exist
        if self.available_models:
            return self.available_models[0]
            
        return preferred_model

    def generate(self, prompt, model_name="gemma2:2b", system_prompt=None, temperature=0.7):
        """
        Calls /api/generate on Ollama for text completion.
        """
        target_model = self.get_best_model(model_name)
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": target_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        if system_prompt:
            payload["system"] = system_prompt
            
        try:
            response = requests.post(url, json=payload, timeout=45)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                return f"Error from Ollama: HTTP {response.status_code} - {response.text}"
        except requests.exceptions.Timeout:
            return "Ollama generation timed out. Please check model loading on your machine."
        except Exception as e:
            return f"Failed to connect to local Ollama: {str(e)}. Make sure Ollama is running (`ollama serve`)."

    def generate_chat(self, messages, model_name="llama3.2:latest", temperature=0.2):
        """
        Calls /api/chat on Ollama for structured conversational analysis.
        """
        target_model = self.get_best_model(model_name)
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": target_model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=45)
            if response.status_code == 200:
                message_content = response.json().get("message", {}).get("content", "").strip()
                return message_content
            else:
                return f"Error from Ollama Chat: HTTP {response.status_code}"
        except requests.exceptions.Timeout:
            return "Ollama Chat timed out."
        except Exception as e:
            return f"Failed to connect to Ollama: {str(e)}"
