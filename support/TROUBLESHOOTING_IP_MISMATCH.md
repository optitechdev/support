# 🔧 Felsökning: IP Address Mismatch

## **Problem identifierat:**
SSL-certifikat mismatch för `support.optitech-sverige.se`, vilket indikerar DNS-konfigurationsproblem.

## **Vanliga orsaker till IP Address Mismatch:**

### **1. CNAME pekar på fel destination**
```bash
# Kontrollera vad din CNAME pekar på
host support.optitech-sverige.se

# Eller använd online-verktyg:
# https://www.whatsmydns.net/#CNAME/support.optitech-sverige.se
```

### **2. Heroku-appen finns inte eller har fel namn**
```bash
# Kontrollera Heroku-appar
heroku apps

# Kontrollera specifik app
heroku info -a optitech-support-system
```

### **3. Domänen är inte tillagd i Heroku**
```bash
# Lista domäner för appen
heroku domains -a optitech-support-system

# Lägg till domän om den saknas
heroku domains:add support.optitech-sverige.se -a optitech-support-system
```

## **Steg-för-steg lösning:**

### **Steg 1: Verifiera Heroku-app status**
```bash
# Logga in på Heroku
heroku login

# Lista alla dina appar
heroku apps

# Om appen inte finns, skapa den
heroku create optitech-support-system

# Kontrollera app-status
heroku ps -a optitech-support-system
```

### **Steg 2: Kontrollera domän-konfiguration**
```bash
# Lista domäner för appen
heroku domains -a optitech-support-system

# Om domänen saknas, lägg till den
heroku domains:add support.optitech-sverige.se -a optitech-support-system

# Kontrollera SSL-status
heroku certs -a optitech-support-system
```

### **Steg 3: Uppdatera DNS-konfiguration**

Gå till din DNS-leverantör (Binero, Loopia, Cloudflare, etc.) och kontrollera:

**Korrekt CNAME-konfiguration:**
```dns
Typ: CNAME
Namn: support
Värde: optitech-support-system.herokuapp.com
TTL: 300
```

**VIKTIGT:** Ta bort eventuella A-records för `support` subdomänen.

### **Steg 4: Verifiera deployment**
```bash
# Kontrollera att appen körs
heroku logs --tail -a optitech-support-system

# Testa Heroku-URL direkt
curl -I https://optitech-support-system.herokuapp.com

# Deploy om nödvändigt
git push heroku main
```

## **Snabb fix - Automatiskt skript:**

Skapa och kör detta automatiska fixskript:

```bash
#!/bin/bash
echo "🔧 Fixar IP Address Mismatch för support.optitech-sverige.se"

# 1. Kontrollera/skapa Heroku-app
heroku apps:info -a optitech-support-system || heroku create optitech-support-system

# 2. Lägg till domän
heroku domains:add support.optitech-sverige.se -a optitech-support-system

# 3. Kontrollera SSL
heroku certs -a optitech-support-system

# 4. Visa DNS-instruktioner
echo ""
echo "✅ Uppdatera din DNS med:"
echo "Typ: CNAME"
echo "Namn: support"  
echo "Värde: optitech-support-system.herokuapp.com"
echo "TTL: 300"

# 5. Testa efter 5 minuter
echo ""
echo "Vänta 5-15 minuter och testa sedan:"
echo "curl -I https://support.optitech-sverige.se"
```

## **DNS-propagering kontroll:**

```bash
# Installera DNS-verktyg om de saknas
apt-get update && apt-get install -y dnsutils

# Kontrollera DNS-propagering
dig support.optitech-sverige.se CNAME

# Eller använd online-verktyg:
# https://www.whatsmydns.net/#CNAME/support.optitech-sverige.se
```

## **Vanliga fel och lösningar:**

### **Fel 1: "SSL: no alternative certificate subject name matches"**
**Orsak:** Domänen är inte tillagd i Heroku eller SSL-certifikat saknas
**Lösning:** 
```bash
heroku domains:add support.optitech-sverige.se -a optitech-support-system
```

### **Fel 2: "Name or service not known"**
**Orsak:** DNS-propagering inte klar eller fel CNAME
**Lösning:** Vänta 15-30 minuter och kontrollera CNAME-post

### **Fel 3: "Connection refused"**
**Orsak:** Heroku-appen körs inte
**Lösning:**
```bash
heroku ps:scale web=1 -a optitech-support-system
heroku restart -a optitech-support-system
```

## **Kontakta support om problemet kvarstår:**

Om du fortfarande har problem efter dessa steg:

1. **Skicka output från:**
   ```bash
   heroku domains -a optitech-support-system
   heroku ps -a optitech-support-system
   ```

2. **Skärmdump av din DNS-konfiguration**

3. **Exakt felmeddelande du får**

Vill du att jag kör det automatiska fixskriptet åt dig?
