#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
import json
from azure_chat_assistant import test_ai_connection

def test_ai_performance():
    """Testar AI-prestanda med olika konfigurationer"""
    print("🚀 Testar AI-prestandaoptimering...")
    print("=" * 50)
    
    # Test 1: Anslutningstest
    print("\n1️⃣ Testar grundläggande anslutning...")
    connection_start = time.time()
    connection_success = test_ai_connection()
    connection_time = time.time() - connection_start
    print(f"   Anslutningstest: {connection_time:.2f}s")
    
    if not connection_success:
        print("❌ Anslutningstest misslyckades. Kontrollera API-nycklar.")
        return
    
    # Test 2: Web API-test (om servern körs)
    print("\n2️⃣ Testar web API-prestanda...")
    test_messages = [
        "Hej, kan du hjälpa mig?",
        "Vad gör Optitech?",
        "Jag behöver support",
        "Tack för hjälpen!"
    ]
    
    total_times = []
    
    for i, message in enumerate(test_messages, 1):
        print(f"   Test {i}: '{message[:30]}...'")
        start_time = time.time()
        
        try:
            response = requests.post('http://localhost:5000/chat', 
                json={
                    'message': message,
                    'conversation_history': []
                },
                timeout=30
            )
            
            end_time = time.time()
            duration = end_time - start_time
            total_times.append(duration)
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"   ✅ Svar på {duration:.2f}s")
                else:
                    print(f"   ❌ API-fel: {data.get('error', 'Okänt fel')}")
            else:
                print(f"   ❌ HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️  Server inte igång - hoppar över web API-test")
            break
        except Exception as e:
            print(f"   ❌ Fel: {str(e)}")
    
    # Resultat
    print("\n📊 RESULTAT:")
    print("=" * 50)
    
    if total_times:
        avg_time = sum(total_times) / len(total_times)
        min_time = min(total_times)
        max_time = max(total_times)
        
        print(f"   Genomsnittlig svarstid: {avg_time:.2f}s")
        print(f"   Snabbaste svar: {min_time:.2f}s")
        print(f"   Långsammaste svar: {max_time:.2f}s")
        
        # Bedömning
        if avg_time < 3:
            print("   🟢 UTMÄRKT prestanda!")
        elif avg_time < 5:
            print("   🟡 BRA prestanda")
        elif avg_time < 10:
            print("   🟠 ACCEPTABEL prestanda")
        else:
            print("   🔴 LÅNGSAM prestanda - behöver optimering")
    
    print(f"\n💡 Tips för att förbättra prestanda:")
    print(f"   • Minska max_tokens för snabbare svar")
    print(f"   • Använd lägre temperature (0.1-0.3)")
    print(f"   • Korta system-meddelanden")
    print(f"   • Implementera caching för vanliga frågor")
    print(f"   • Använd connection pooling")

if __name__ == "__main__":
    test_ai_performance()
