import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = "https://yazan-me7jxcy8-eastus2.cognitiveservices.azure.com/"
DEPLOYMENT_NAME = "gpt-4.1"
API_VERSION = "2025-01-01-preview"

def test_ai_connection():
    """Testar anslutning till Azure OpenAI"""
    url = f"{ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    data = {
        "messages": [
            {"role": "system", "content": "Du är en hjälpsam AI-assistent på svenska."},
            {"role": "user", "content": "Säg hej och bekräfta att du fungerar!"}
        ],
        "temperature": 0.3,  # Lägre temperatur för snabbare svar
        "max_tokens": 500,   # Öka lite för bättre svar
        "top_p": 0.9
    }

    print("🔄 Testar AI-anslutning...")
    response = requests.post(url, headers=headers, json=data, timeout=10)  # 10 sekunders timeout

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        print(f"✅ AI fungerar! Svar: {reply}")
        return True
    else:
        print(f"❌ Fel {response.status_code}: {response.text}")
        return False

if __name__ == "__main__":
    test_ai_connection()
