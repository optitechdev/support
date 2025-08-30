#!/bin/bash

# Heroku Deployment Script för support.optitech-sverige.se
# Kör detta script för att deploya till Heroku

echo "🚀 Deploying Optitech Support to support.optitech-sverige.se"
echo "=================================================="

# Kontrollera att Heroku CLI är installerat
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI är inte installerat. Installera från: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Logga in på Heroku
echo "🔐 Loggar in på Heroku..."
heroku login

# Skapa Heroku-app
echo "📦 Skapar Heroku-app..."
heroku create optitech-support-system

# Sätt miljövariabler
echo "⚙️ Sätter miljövariabler..."
echo "Ange din Azure OpenAI API-nyckel:"
read -s AZURE_KEY
heroku config:set AZURE_OPENAI_API_KEY="$AZURE_KEY"

echo "Ange din SendGrid API-nyckel:"
read -s SENDGRID_KEY
heroku config:set SENDGRID_API_KEY="$SENDGRID_KEY"

heroku config:set FLASK_ENV=production

# Deploya
echo "🚀 Deployar till Heroku..."
git push heroku main

# Lägg till subdomän
echo "🌐 Lägger till subdomän..."
heroku domains:add support.optitech-sverige.se

# Visa DNS-information
echo ""
echo "✅ Deployment klar!"
echo "=================================================="
echo "Nu behöver du lägga till denna CNAME-post hos din DNS-leverantör:"
echo ""
echo "Typ: CNAME"
echo "Namn: support"
echo "Värde: optitech-support-system.herokuapp.com"
echo "TTL: 300"
echo ""
echo "App URL: https://optitech-support-system.herokuapp.com"
echo "Din domän (efter DNS-uppdatering): https://support.optitech-sverige.se"
echo ""
echo "Kontrollera status med: heroku domains"
