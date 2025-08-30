import os
import requests
import uuid
import datetime
import json
import re
from dotenv import load_dotenv
from optitech_supportmail import send_support_email

load_dotenv()

API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = "https://yazan-me7jxcy8-eastus2.cognitiveservices.azure.com/"
DEPLOYMENT_NAME = "gpt-4.1"
API_VERSION = "2025-01-01-preview"

url = f"{ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

class AISupport:
    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": """Du är en vänlig AI-assistent för Optitech Sverige. 

VIKTIGT: Du ska FÖRST chatta naturligt med kunden och hjälpa dem så gott du kan. 
Svara på frågor, lös problem och ge teknisk support.

BARA när kunden uttryckligen ber om att "skapa ett ärende" eller "öppna ett supportärende" 
ELLER när du inte kan lösa problemet själv, då ska du samla in:
- Kundens namn  
- E-postadress
- Kort beskrivning av problemet

När du har all denna info, svara EXAKT: "SKAPA_ÄRENDE: [namn] | [email] | [beskrivning]"

Annars - chatta bara normalt och hjälp kunden så gott du kan!"""
            }
        ]
        
    def extract_ticket_data(self, ai_response):
        """Extraherar ärendedata från AI:ns svar"""
        pattern = r"SKAPA_ÄRENDE:\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*(.+)"
        match = re.search(pattern, ai_response)
        
        if match:
            return {
                "namn": match.group(1).strip(),
                "email": match.group(2).strip(), 
                "beskrivning": match.group(3).strip()
            }
        return None
    
    def chat_with_ai(self, user_input):
        """Skickar meddelande till AI och får svar"""
        self.messages.append({"role": "user", "content": user_input})
        
        response = requests.post(url, headers=headers, json={
            "messages": self.messages,
            "temperature": 0.7,
            "max_tokens": 1500
        })
        
        if response.status_code == 200:
            ai_reply = response.json()["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": ai_reply})
            return ai_reply
        else:
            return f"❌ Fel vid kommunikation med AI: {response.status_code}"
    
    def create_support_ticket(self, ticket_data):
        """Skapar supportärende och skickar e-post"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        ticket_id = f"OPT-{timestamp}-{uuid.uuid4().hex[:4].upper()}"
        
        print(f"\n🎫 Skapar supportärende: {ticket_id}")
        
        # Skicka e-post
        send_support_email(
            customer_name=ticket_data["namn"],
            customer_email=ticket_data["email"], 
            ticket_description=ticket_data["beskrivning"],
            ticket_id=ticket_id
        )
        
        return ticket_id
    
    def start_chat(self):
        """Startar chattsessionen"""
        print("💬 Hej! Jag är din AI-assistent från Optitech Sverige.")
        print("💡 Ställ dina frågor så hjälper jag dig så gott jag kan!")
        print("📝 Skriv 'sluta' för att avsluta.\n")
        
        while True:
            user_input = input("🧑 Du: ").strip()
            
            if user_input.lower() in ["sluta", "avsluta", "exit"]:
                print("👋 Tack för att du använde vår support! Ha en bra dag!")
                break
                
            if not user_input:
                continue
                
            # Få AI:ns svar
            ai_response = self.chat_with_ai(user_input)
            
            # Kolla om AI vill skapa ett ärende
            ticket_data = self.extract_ticket_data(ai_response)
            
            if ticket_data:
                # Ta bort SKAPA_ÄRENDE delen från svaret
                clean_response = re.sub(r"SKAPA_ÄRENDE:[^|]+\|[^|]+\|.+", "", ai_response).strip()
                if clean_response:
                    print(f"\n🤖 AI: {clean_response}")
                
                # Skapa ärendet
                ticket_id = self.create_support_ticket(ticket_data)
                print(f"✅ Supportärende {ticket_id} har skapats och e-post är skickad!")
                print("📧 Du kommer få en bekräftelse på din e-post inom kort.")
                break
            else:
                # Normal chat - visa AI:ns svar
                print(f"\n🤖 AI: {ai_response}")

if __name__ == "__main__":
    support_ai = AISupport()
    support_ai.start_chat()
