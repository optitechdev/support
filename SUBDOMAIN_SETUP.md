# 🌐 Subdomän Setup: support.optitech-sverige.se

## **DNS-konfiguration för subdomän**

Eftersom du vill använda `support.optitech-sverige.se` behöver du bara lägga till en CNAME-post i din DNS-konfiguration för `optitech-sverige.se`.

### **Steg 1: Hosting-setup (Heroku rekommenderat)**

```bash
# 1. Skapa Heroku-app med specifikt namn
heroku create optitech-support-system

# 2. Sätt miljövariabler
heroku config:set AZURE_OPENAI_API_KEY="din-azure-openai-nyckel"
heroku config:set SENDGRID_API_KEY="din-sendgrid-nyckel"
heroku config:set FLASK_ENV=production

# 3. Deploya
git push heroku main

# 4. Lägg till subdomänen
heroku domains:add support.optitech-sverige.se

# 5. Kontrollera DNS-target
heroku domains
```

### **Steg 2: DNS-konfiguration hos din registrar**

Logga in på kontrollpanelen där du hanterar `optitech-sverige.se` och lägg till:

```dns
Typ: CNAME
Namn: support
Värde: optitech-support-system.herokuapp.com
TTL: 300 (5 minuter)
```

**ELLER om du använder DigitalOcean:**
```dns
Typ: CNAME  
Namn: support
Värde: optitech-support-system-12345.ondigitalocean.app
TTL: 300
```

### **Steg 3: SSL-certifikat**

Heroku ger automatiskt SSL för subdomäner, så `https://support.optitech-sverige.se` kommer fungera direkt.

### **Steg 4: Exempel för olika registrars**

#### **Om du använder Binero:**
1. Gå till "Domäner" → "optitech-sverige.se" → "DNS"
2. Lägg till ny post:
   ```
   Typ: CNAME
   Namn: support  
   Innehåll: optitech-support-system.herokuapp.com
   TTL: 300
   ```

#### **Om du använder Loopia:**
1. Gå till "Kundzon" → "Domäner" → "optitech-sverige.se"
2. Klicka "DNS-inställningar"
3. Lägg till:
   ```
   support CNAME optitech-support-system.herokuapp.com
   ```

#### **Om du använder Cloudflare:**
1. Gå till DNS-fliken för `optitech-sverige.se`
2. Lägg till:
   ```
   Type: CNAME
   Name: support
   Content: optitech-support-system.herokuapp.com
   Proxy status: Proxied (orange cloud) 
   ```

### **Steg 5: Testa konfigurationen**

```bash
# Kontrollera DNS (kan ta 5-60 min att propagera)
nslookup support.optitech-sverige.se

# Eller använd online-verktyg:
# https://www.whatsmydns.net/#CNAME/support.optitech-sverige.se
```

## **Deployment till Heroku steg-för-steg:**

### **1. Installera Heroku CLI**
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Ladda ner från: https://devcenter.heroku.com/articles/heroku-cli

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh
```

### **2. Logga in och skapa app**
```bash
heroku login
heroku create optitech-support-system
```

### **3. Sätt miljövariabler**
```bash
heroku config:set AZURE_OPENAI_API_KEY="din-azure-openai-api-nyckel"
heroku config:set SENDGRID_API_KEY="din-sendgrid-api-nyckel"  
heroku config:set FLASK_ENV=production
```

### **4. Deploya från ditt GitHub-repo**
```bash
git push heroku main
```

### **5. Lägg till subdomänen**
```bash
heroku domains:add support.optitech-sverige.se
```

### **6. Kontrollera status**
```bash
heroku domains
heroku logs --tail
```

## **Alternativ: DigitalOcean App Platform**

Om du föredrar DigitalOcean:

1. Gå till [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Koppla ditt GitHub-repo: `optitechdev/support`
3. Sätt miljövariabler i Settings
4. Lägg till domän: `support.optitech-sverige.se`
5. Få DNS-target och uppdatera CNAME

## **Tidsram:**

- **Heroku deployment:** 5-10 minuter
- **DNS-propagering:** 5-60 minuter  
- **SSL-aktivering:** Automatisk på Heroku

## **Kostnad:**

- **Heroku Eco Plan:** $5/månad
- **DigitalOcean Basic:** $5/månad
- **Ingen extra kostnad för subdomän**

## **Felsökning:**

### **Om subdomänen inte fungerar:**
```bash
# Kontrollera DNS
dig support.optitech-sverige.se CNAME

# Kontrollera Heroku-app
heroku ps
heroku logs
```

### **Vanliga fel:**
- **TTL för hög:** Sätt TTL till 300 sekunder
- **Fel CNAME-värde:** Kontrollera exakt Heroku-app-namn
- **Cachade DNS:** Vänta eller rensa DNS-cache

## **Nästa steg:**

1. ✅ Välj Heroku eller DigitalOcean
2. ✅ Deploya appen  
3. ✅ Lägg till CNAME-post hos din registrar
4. ✅ Vänta på DNS-propagering
5. ✅ Testa `https://support.optitech-sverige.se`

Vill du att jag hjälper dig sätta upp Heroku deployment nu?
