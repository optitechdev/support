# ✅ DNS-konfiguration bekräftad!

## **Status för support.optitech-sverige.se**

Du har fått följande DNS-information:
- **Domän:** support.optitech-sverige.se  
- **CNAME:** optitech-support-system.herokuapp.com

## **Nästa steg: Deploya till Heroku**

### **Snabbstart (om du har Heroku CLI installerat):**

```bash
# 1. Logga in på Heroku
heroku login

# 2. Skapa appen med exakt samma namn
heroku create optitech-support-system

# 3. Sätt miljövariabler
heroku config:set AZURE_OPENAI_API_KEY="din-azure-openai-nyckel"
heroku config:set SENDGRID_API_KEY="din-sendgrid-nyckel"
heroku config:set FLASK_ENV=production

# 4. Deploya
git push heroku main

# 5. Lägg till domänen
heroku domains:add support.optitech-sverige.se

# 6. Kontrollera status
heroku domains
heroku ps:scale web=1
```

### **Eller använd vårt automatiska skript:**

```bash
./deploy.sh
```

## **Verifiera deployment:**

```bash
# Kontrollera Heroku-app
curl https://optitech-support-system.herokuapp.com

# Kontrollera din domän (efter DNS-propagering)
curl https://support.optitech-sverige.se
```

## **DNS-propagering:**

DNS-ändringar tar vanligtvis:
- **5-15 minuter** för de flesta DNS-servrar
- **Upp till 48 timmar** för fullständig global propagering

Du kan kontrollera status på: https://www.whatsmydns.net/#CNAME/support.optitech-sverige.se

## **Felsökning:**

Om domänen inte fungerar direkt:
1. **Vänta 15-30 minuter** på DNS-propagering
2. **Kontrollera CNAME-posten** hos din registrar
3. **Rensa DNS-cache:** `ipconfig /flushdns` (Windows) eller `sudo dscacheutil -flushcache` (Mac)

Vill du att jag hjälper dig köra deployment nu?
