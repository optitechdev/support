# Azure OpenAI på GitHub Pages - Deployment Guide

## 🚀 Steg 1: Skapa Netlify konto och site

1. Gå till [netlify.com](https://netlify.com) och skapa konto
2. Koppla ditt GitHub-repo `optitechdev/support`
3. Sätt som build command: `echo "No build needed"`
4. Sätt publish directory: `.` (root)

## 🔑 Steg 2: Konfigurera miljövariabler i Netlify

Gå till Site settings > Environment variables och lägg till:

```
AZURE_OPENAI_API_KEY=din_azure_openai_api_nyckel
AZURE_OPENAI_ENDPOINT=https://yazan-me7jxcy8-eastus2.cognitiveservices.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

## 🌐 Steg 3: Uppdatera DNS för Netlify

1. I Netlify: Site settings > Domain management
2. Lägg till custom domain: `support.optitech-sverige.se`
3. Följ instruktionerna för DNS-konfiguration

**ELLER** använd Netlify som proxy:

## 🔄 Alternativ: Behåll GitHub Pages som primär

1. Deploya även till Netlify med subdomain (t.ex. `api.optitech-sverige.se`)
2. Uppdatera API URL i HTML:
   ```javascript
   const apiUrl = 'https://api.optitech-sverige.se/.netlify/functions/chat';
   ```

## 📁 Filer som behövs:

- ✅ `netlify/functions/chat.js` - Serverless function
- ✅ `netlify.toml` - Netlify konfiguration  
- ✅ `package.json` - Dependencies
- ✅ Uppdaterad `index.html` - Med ny API-integration

## 🧪 Testa lokalt:

```bash
npm install netlify-cli -g
netlify dev
```

## 🎯 Resultat:

✅ **GitHub Pages**: Snabb statisk hosting
✅ **Netlify Functions**: Riktig Azure OpenAI
✅ **Din domän**: support.optitech-sverige.se
✅ **Riktig AI**: Serverless Azure OpenAI integration

---

**OBS:** Du kan också använda Vercel, Railway eller andra serverless providers med samma princip!
