# 🌐 Guide: Koppla din domän till Optitech Support

## **Steg 1: Välj Hosting-tjänst**

### **Alternativ A: Heroku (Rekommenderat för början)**
```bash
# 1. Installera Heroku CLI
# Ladda ner från: https://devcenter.heroku.com/articles/heroku-cli

# 2. Logga in på Heroku
heroku login

# 3. Skapa Heroku-app
heroku create optitech-support-app

# 4. Sätt miljövariabler
heroku config:set AZURE_OPENAI_API_KEY="din-api-nyckel"
heroku config:set SENDGRID_API_KEY="din-sendgrid-nyckel"

# 5. Deploya
git push heroku main

# 6. Lägg till din domän
heroku domains:add din-domän.se
```

### **Alternativ B: DigitalOcean App Platform**
```bash
# 1. Pusha kod till GitHub (redan gjort)
# 2. Gå till DigitalOcean App Platform
# 3. Koppla ditt GitHub repo
# 4. Lägg till miljövariabler
# 5. Lägg till din domän i settings
```

### **Alternativ C: Vercel (För enklare deployment)**
```bash
# 1. Installera Vercel CLI
npm i -g vercel

# 2. Logga in
vercel login

# 3. Deploya
vercel

# 4. Lägg till domän
vercel domains add din-domän.se
```

## **Steg 2: DNS-konfiguration**

### **Om du har din domän hos någon registrar (Binero, Loopia, etc.):**

1. **Logga in på din domänregistrars kontrollpanel**

2. **Lägg till DNS-poster:**
   ```
   Typ: CNAME
   Namn: www
   Värde: [hosting-url från Heroku/DigitalOcean/Vercel]
   
   Typ: A eller ALIAS (för apex-domän)
   Namn: @
   Värde: [IP-adress från hosting-tjänsten]
   ```

3. **För Heroku specifikt:**
   ```
   CNAME: www -> din-app-namn.herokuapp.com
   ALIAS: @ -> din-app-namn.herokuapp.com
   ```

### **Exempel DNS-inställningar:**
```
Host: @
Type: ALIAS
Value: optitech-support-app.herokuapp.com

Host: www  
Type: CNAME
Value: optitech-support-app.herokuapp.com
```

## **Steg 3: SSL-certifikat**

Alla moderna hosting-tjänster ger gratis SSL automatiskt:
- ✅ Heroku: Automatisk SSL
- ✅ DigitalOcean: Gratis Let's Encrypt
- ✅ Vercel: Automatisk SSL

## **Steg 4: Testa deployment lokalt först**

```bash
# 1. Installera beroenden
pip install -r requirements.txt

# 2. Sätt miljövariabler (skapa .env fil)
AZURE_OPENAI_API_KEY=din-nyckel
SENDGRID_API_KEY=din-sendgrid-nyckel

# 3. Kör lokalt
python app.py

# 4. Testa på http://localhost:5000
```

## **Steg 5: Domän-exempel för olika tjänster**

### **Binero DNS-inställningar:**
```
Namn: @
Typ: ALIAS  
Innehåll: optitech-support-app.herokuapp.com
TTL: 300

Namn: www
Typ: CNAME
Innehåll: optitech-support-app.herokuapp.com  
TTL: 300
```

### **Cloudflare DNS-inställningar:**
```
Type: CNAME
Name: @
Content: optitech-support-app.herokuapp.com
Proxy status: Proxied (orange cloud)

Type: CNAME  
Name: www
Content: optitech-support-app.herokuapp.com
Proxy status: Proxied (orange cloud)
```

## **Steg 6: Miljövariabler för produktion**

Skapa dessa miljövariabler i din hosting-tjänst:

```bash
AZURE_OPENAI_API_KEY=din-azure-openai-nyckel
SENDGRID_API_KEY=din-sendgrid-api-nyckel
FLASK_ENV=production
PORT=5000
```

## **Kommande steg för deployment:**

1. **Välj hosting-tjänst**
2. **Sätt upp miljövariabler** 
3. **Deploya koden**
4. **Konfigurera DNS**
5. **Testa att allt fungerar**

## **Kostnader:**

- **Heroku:** Gratis tier (begränsningar), $7/mån för basic
- **DigitalOcean:** $5/mån för basic app
- **Vercel:** Gratis för små projekt
- **Domän:** ~100-200 kr/år

Vill du att jag hjälper dig sätta upp någon specifik hosting-tjänst?
