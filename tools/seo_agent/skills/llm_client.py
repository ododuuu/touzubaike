
import os
import json
import sys

# Simple abstraction for LLM calls
# In a real deployment, this would use openai/google-generativeai libraries
def call_llm(prompt: str, model: str = "gemini-3-pro-preview") -> str:
    """
    Simulates or performs an LLM call. 
    Checks for API keys in environment variables.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("WARNING: GEMINI_API_KEY not found. Returning mock data.", file=sys.stderr)
        return "MOCKED_LLM_RESPONSE"

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        import urllib.request
        import urllib.error
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            # Safe extraction
            if "candidates" in result and result["candidates"]:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return ""  # Blocked or empty
                
    except urllib.error.HTTPError as e:
        print(f"LLM API Error: {e.code} {e.reason}", file=sys.stderr)
        print(f"Response Body: {e.read().decode('utf-8')}", file=sys.stderr)
        return "MOCKED_LLM_RESPONSE"
    except Exception as e:
        print(f"LLM API Error: {e}", file=sys.stderr)
        return "MOCKED_LLM_RESPONSE"

def parse_json_response(response_text: str) -> dict:
    """
    Cleans and extracts JSON from LLM response (handling markdown fences).
    """
    cleaned = response_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return json.loads(cleaned.strip())
