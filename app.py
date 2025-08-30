#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import requests
import uuid
import datetime
import json
import re
from dotenv import load_dotenv
from optitech_supportmail import send_support_email

load_dotenv()

app = Flask(__name__)
CORS(app)

# Azure OpenAI konfiguration
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = "https://yazan-me7jxcy8-eastus2.cognitiveservices.azure.com/"
DEPLOYMENT_NAME = "gpt-4.1"
API_VERSION = "2025-01-01-preview"

url = f"{ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

class WebAISupport:
    def __init__(self):
        self.system_message = {
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
    
    def chat_with_ai(self, user_input, conversation_history):
        """Skickar meddelande till AI och får svar"""
        messages = [self.system_message] + conversation_history + [{"role": "user", "content": user_input}]
        
        try:
            response = requests.post(url, headers=headers, json={
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1500
            })
            
            if response.status_code == 200:
                ai_reply = response.json()["choices"][0]["message"]["content"]
                return ai_reply
            else:
                return f"❌ Fel vid kommunikation med AI: {response.status_code}"
        except Exception as e:
            return f"❌ Tekniskt fel: {str(e)}"
    
    def create_support_ticket(self, ticket_data):
        """Skapar supportärende och skickar e-post"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        ticket_id = f"OPT-{timestamp}-{uuid.uuid4().hex[:4].upper()}"
        
        try:
            send_support_email(
                customer_name=ticket_data["namn"],
                customer_email=ticket_data["email"], 
                ticket_description=ticket_data["beskrivning"],
                ticket_id=ticket_id
            )
            return ticket_id, True
        except Exception as e:
            print(f"Fel vid e-postsändning: {e}")
            return ticket_id, False

# Global instans
support_ai = WebAISupport()

# HTML template för webbgränssnittet
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Optitech Support - AI Assistent</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 800px;
            height: 600px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 14px;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            animation: fadeIn 0.3s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message {
            background: #667eea;
            color: white;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            margin-left: auto;
            max-width: 70%;
        }
        
        .ai-message {
            background: white;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            margin-right: auto;
            max-width: 70%;
            border: 1px solid #e9ecef;
        }
        
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 10px;
        }
        
        #messageInput {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            outline: none;
            font-size: 14px;
        }
        
        #messageInput:focus {
            border-color: #667eea;
        }
        
        #sendButton {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s;
        }
        
        #sendButton:hover {
            background: #5a6fd8;
        }
        
        #sendButton:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .ticket-success {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #c3e6cb;
            margin: 10px 0;
        }
        
        .loading {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #666;
        }
        
        .loading::after {
            content: '';
            width: 20px;
            height: 20px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h1>🤖 Optitech Support</h1>
            <p>Din AI-assistent för teknisk support • support.optitech-sverige.se</p>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message">
                <div class="ai-message">
                    💬 Hej! Jag är din AI-assistent från Optitech Sverige.<br>
                    💡 Ställ dina frågor så hjälper jag dig så gott jag kan!
                </div>
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Skriv ditt meddelande här..." maxlength="500">
            <button id="sendButton">Skicka</button>
        </div>
    </div>

    <script>
        let conversationHistory = [];
        
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        
        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message';
            
            const messageContent = document.createElement('div');
            messageContent.className = isUser ? 'user-message' : 'ai-message';
            messageContent.innerHTML = content.replace(/\\n/g, '<br>');
            
            messageDiv.appendChild(messageContent);
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function showLoading() {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message';
            loadingDiv.id = 'loading-message';
            
            const loadingContent = document.createElement('div');
            loadingContent.className = 'ai-message loading';
            loadingContent.textContent = 'AI tänker...';
            
            loadingDiv.appendChild(loadingContent);
            chatMessages.appendChild(loadingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function hideLoading() {
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                loadingMessage.remove();
            }
        }
        
        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            // Visa användarens meddelande
            addMessage(message, true);
            conversationHistory.push({role: 'user', content: message});
            
            // Rensa input och visa loading
            messageInput.value = '';
            sendButton.disabled = true;
            showLoading();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        history: conversationHistory
                    })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.success) {
                    addMessage(data.response);
                    conversationHistory.push({role: 'assistant', content: data.response});
                    
                    if (data.ticket_created) {
                        addMessage(`
                            <div class="ticket-success">
                                ✅ <strong>Supportärende ${data.ticket_id} har skapats!</strong><br>
                                📧 Du kommer få en bekräftelse på din e-post inom kort.
                            </div>
                        `);
                    }
                } else {
                    addMessage('❌ Något gick fel. Försök igen senare.');
                }
                
            } catch (error) {
                hideLoading();
                addMessage('❌ Anslutningsfel. Kontrollera din internetanslutning.');
            }
            
            sendButton.disabled = false;
            messageInput.focus();
        }
        
        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        messageInput.focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Visar huvudsidan"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """API-endpoint för chat"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        # Få AI:ns svar
        ai_response = support_ai.chat_with_ai(user_message, conversation_history)
        
        # Kolla om AI vill skapa ett ärende
        ticket_data = support_ai.extract_ticket_data(ai_response)
        
        response_data = {
            'success': True,
            'response': ai_response,
            'ticket_created': False
        }
        
        if ticket_data:
            # Ta bort SKAPA_ÄRENDE delen från svaret
            clean_response = re.sub(r"SKAPA_ÄRENDE:[^|]+\|[^|]+\|.+", "", ai_response).strip()
            if clean_response:
                response_data['response'] = clean_response
            else:
                response_data['response'] = "Jag skapar ett supportärende åt dig nu..."
            
            # Skapa ärendet
            ticket_id, email_sent = support_ai.create_support_ticket(ticket_data)
            response_data['ticket_created'] = True
            response_data['ticket_id'] = ticket_id
            response_data['email_sent'] = email_sent
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    """Hälsokontroll för deployment"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
