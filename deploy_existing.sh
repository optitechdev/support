#!/bin/bash

# 🚀 Deployment guide för support.optitech-sverige.se
# Kör detta på din lokala maskin (inte i Codespace)

echo "🎯 Deployment till befintlig Heroku-app: optitech-support-system"
echo "================================================================"

# Kontrollera Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI behöver installeras först:"
    echo "   Mac: brew install heroku/brew/heroku"
    echo "   Windows: Ladda ner från https://devcenter.heroku.com/articles/heroku-cli"
    echo "   Ubuntu: curl https://cli-assets.heroku.com/install.sh | sh"
    exit 1
fi

echo "🔐 Steg 1: Logga in på Heroku"
heroku login

echo "🔗 Steg 2: Koppla till befintlig app"
heroku git:remote -a optitech-support-system

echo "⚙️ Steg 3: Sätt miljövariabler"
echo "Ange din Azure OpenAI API-nyckel:"
read -s AZURE_KEY
heroku config:set AZURE_OPENAI_API_KEY="$AZURE_KEY"

echo "Ange din SendGrid API-nyckel:"
read -s SENDGRID_KEY
heroku config:set SENDGRID_API_KEY="$SENDGRID_KEY"

heroku config:set FLASK_ENV=production

echo "🚀 Steg 4: Deploya koden"
git push heroku main

echo "🌐 Steg 5: Verifiera domän"
heroku domains

echo ""
echo "✅ Deployment klar!"
echo "================================================================"
echo "App URL: https://optitech-support-system.herokuapp.com"
echo "Din domän: https://support.optitech-sverige.se"
echo ""
echo "DNS-propagering kan ta 5-60 minuter."
echo "Kontrollera status: https://www.whatsmydns.net/#CNAME/support.optitech-sverige.se"
