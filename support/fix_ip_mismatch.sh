#!/bin/bash

# 🔧 Snabb fix för IP Address Mismatch
# support.optitech-sverige.se

echo "🔧 Fixar IP Address Mismatch för support.optitech-sverige.se"
echo "============================================================"

# Kontrollera att vi är inloggade på Heroku
echo "📋 Kontrollerar Heroku-inloggning..."
if ! heroku auth:whoami &>/dev/null; then
    echo "❌ Inte inloggad på Heroku. Loggar in..."
    heroku login
fi

# Kontrollera om appen finns, skapa annars
echo "📦 Kontrollerar Heroku-app..."
if heroku apps:info -a optitech-support-system &>/dev/null; then
    echo "✅ App 'optitech-support-system' finns redan"
else
    echo "🆕 Skapar ny Heroku-app 'optitech-support-system'..."
    heroku create optitech-support-system
fi

# Lägg till domänen om den inte finns
echo "🌐 Kontrollerar domän-konfiguration..."
if heroku domains -a optitech-support-system | grep -q "support.optitech-sverige.se"; then
    echo "✅ Domän 'support.optitech-sverige.se' är redan tillagd"
else
    echo "➕ Lägger till domän 'support.optitech-sverige.se'..."
    heroku domains:add support.optitech-sverige.se -a optitech-support-system
fi

# Kontrollera SSL-certifikat
echo "🔒 Kontrollerar SSL-certifikat..."
heroku certs -a optitech-support-system

# Kontrollera att appen körs
echo "🚀 Kontrollerar app-status..."
heroku ps -a optitech-support-system

# Starta appen om den inte körs
if ! heroku ps -a optitech-support-system | grep -q "web.1: up"; then
    echo "🔄 Startar web dyno..."
    heroku ps:scale web=1 -a optitech-support-system
fi

echo ""
echo "✅ Heroku-konfiguration klar!"
echo "============================================================"
echo ""
echo "🔧 NÄSTA STEG - Uppdatera din DNS:"
echo ""
echo "Gå till din DNS-leverantör och sätt:"
echo "  Typ: CNAME"
echo "  Namn: support"
echo "  Värde: optitech-support-system.herokuapp.com"
echo "  TTL: 300"
echo ""
echo "🕐 Vänta 5-15 minuter på DNS-propagering"
echo ""
echo "✅ Testa sedan med:"
echo "  curl -I https://support.optitech-sverige.se"
echo ""
echo "📊 Övervaka DNS-propagering på:"
echo "  https://www.whatsmydns.net/#CNAME/support.optitech-sverige.se"
echo ""

# Visa nuvarande domän-status
echo "📋 Nuvarande domän-konfiguration:"
heroku domains -a optitech-support-system
