
import os
import sys
import urllib.request
import json

def list_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API Key found.")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("Available Models:")
            for m in data.get('models', []):
                print(f"- {m['name']}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
