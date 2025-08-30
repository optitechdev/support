# 🚀 Netlify Deployment Guide

## Snabbdeployment

### 1. Automatisk deployment via Git
```bash
# Säkerställ att alla ändringar är committade
git add .
git commit -m "Optimerad AI-prestanda för Netlify"
git push origin main
```

### 2. Manuell deployment via CLI
```bash
# Logga in på Netlify (första gången)
netlify login

# Bygg och deployer
netlify deploy --prod

# Eller bara deployer utan build
netlify deploy --prod --dir .
```

## Miljövariabler som behöver konfigureras på Netlify:

1. **AZURE_OPENAI_API_KEY** - Din Azure OpenAI API-nyckel
2. **AZURE_OPENAI_ENDPOINT** - https://yazan-me7jxcy8-eastus2.cognitiveservices.azure.com/
3. **AZURE_OPENAI_DEPLOYMENT** - gpt-4.1
4. **AZURE_OPENAI_API_VERSION** - 2025-01-01-preview

## Steg-för-steg på Netlify.com:

### 1. Logga in på https://app.netlify.com/
### 2. Gå till din site
### 3. Gå till "Site settings" → "Environment variables"
### 4. Lägg till miljövariablerna ovan
### 5. Gå till "Deploys" → "Trigger deploy" → "Deploy site"

## Optimeringar som gjorts:

✅ **AI-prestanda optimerad:**
- Temperature: 0.7 → 0.3 (snabbare svar)
- Max tokens: 1500 → 800 (kortare svar)
- Timeout: 15 sekunder
- Kortare system-prompts

✅ **Serverless function uppdaterad:**
- Optimerade AI-parametrar
- Bättre felhantering
- CORS-support

## Testa deployment:

```bash
# Kör lokalt först
netlify dev

# Testa funktionen
curl -X POST http://localhost:8888/.netlify/functions/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hej, kan du hjälpa mig?"}'
```

## Troubleshooting:

**Problem: Function timeout**
- Lösning: Miljövariablerna är inte konfigurerade

**Problem: CORS-fel**
- Lösning: Kontrollera att headers är korrekt satta

**Problem: Långsam AI**
- Lösning: De nya optimerade parametrarna ska lösa detta
