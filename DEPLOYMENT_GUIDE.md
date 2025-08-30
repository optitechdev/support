# 🚀 Deployment till support.optitech-sverige.se

## **Situation:**
✅ Heroku-app `optitech-support-system` är skapad  
✅ DNS CNAME är konfigurerad: `optitech-support-system.herokuapp.com`  
⏳ Behöver deploya koden

## **Steg-för-steg deployment:**

### **1. På din lokala maskin (inte Codespace):**

```bash
# Klona projektet
git clone https://github.com/optitechdev/support.git
cd support

# Koppla till Heroku-appen
heroku git:remote -a optitech-support-system

# Sätt miljövariabler
heroku config:set AZURE_OPENAI_API_KEY="din-azure-nyckel"
heroku config:set SENDGRID_API_KEY="din-sendgrid-nyckel"
heroku config:set FLASK_ENV=production

# Deploya
git push heroku main
```

### **2. Eller kör vårt automatiska skript:**

```bash
./deploy_existing.sh
```

## **Kontrollera status:**

```bash
# Kontrollera Heroku-app
heroku ps
heroku logs --tail

# Testa appen
curl https://optitech-support-system.herokuapp.com
```

## **Efter deployment:**

1. **Heroku-app:** https://optitech-support-system.herokuapp.com
2. **Din domän:** https://support.optitech-sverige.se (efter DNS-propagering)

## **DNS-propagering:**

- **CNAME-post:** `support` → `optitech-support-system.herokuapp.com`
- **Tid:** 5-60 minuter
- **Kontroll:** https://www.whatsmydns.net/#CNAME/support.optitech-sverige.se

## **Om du inte har Heroku CLI:**

### **Installera Heroku CLI:**

**Mac:**
```bash
brew install heroku/brew/heroku
```

**Windows:**
Ladda ner från: https://devcenter.heroku.com/articles/heroku-cli

**Ubuntu/Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

## **Felsökning:**

### **Om deployment misslyckas:**
```bash
heroku logs --tail
heroku ps:restart
```

### **Om domänen inte fungerar:**
1. Vänta 30 minuter på DNS-propagering
2. Kontrollera CNAME-posten hos registrar
3. Testa: `curl -I https://support.optitech-sverige.se`

## **Nästa steg:**

1. ✅ Klona repo lokalt
2. ✅ Koppla till Heroku-app
3. ✅ Sätt miljövariabler
4. ✅ Deploya med `git push heroku main`
5. ✅ Vänta på DNS och testa domänen

**Allt är förberett - du behöver bara köra deployment! 🚀**
