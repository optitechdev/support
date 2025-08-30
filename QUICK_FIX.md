# 🚨 LÖSNING: Deploya koden till Heroku

## **Problem:**
✅ DNS fungerar: `support.optitech-sverige.se` → `optitech-support-system.herokuapp.com`  
❌ Heroku-appen är tom: "There's nothing here, yet."

## **Lösning: Deploya koden**

### **På din lokala dator (INTE i Codespace):**

```bash
# 1. Klona projektet (om du inte har det)
git clone https://github.com/optitechdev/support.git
cd support

# 2. Installera Heroku CLI (om du inte har det)
# Mac: brew install heroku/brew/heroku
# Windows: Ladda ner från https://devcenter.heroku.com/articles/heroku-cli

# 3. Logga in på Heroku
heroku login

# 4. Koppla till befintlig app
heroku git:remote -a optitech-support-system

# 5. Sätt miljövariabler
heroku config:set AZURE_OPENAI_API_KEY="din-azure-openai-nyckel"
heroku config:set SENDGRID_API_KEY="din-sendgrid-nyckel"
heroku config:set FLASK_ENV=production

# 6. Deploya koden
git push heroku main

# 7. Kontrollera att det fungerar
heroku ps:scale web=1
heroku open
```

## **Eller via Heroku Dashboard (webbläsare):**

1. Gå till: https://dashboard.heroku.com/apps/optitech-support-system
2. Klicka på "Deploy" fliken
3. Under "Deployment method" välj "GitHub"
4. Koppla till ditt repo: `optitechdev/support`
5. Klicka "Deploy Branch" från `main`

## **Sätt miljövariabler via Dashboard:**

1. Gå till "Settings" fliken
2. Klicka "Reveal Config Vars"
3. Lägg till:
   ```
   AZURE_OPENAI_API_KEY = din-azure-openai-nyckel
   SENDGRID_API_KEY = din-sendgrid-nyckel
   FLASK_ENV = production
   ```

## **Efter deployment:**

- **Heroku-app:** https://optitech-support-system.herokuapp.com
- **Din domän:** https://support.optitech-sverige.se

Båda ska visa din AI Support-app istället för "There's nothing here, yet."

## **Snabb-test:**

```bash
# Testa Heroku-appen
curl https://optitech-support-system.herokuapp.com

# Testa din domän
curl https://support.optitech-sverige.se
```

## **Felsökning:**

Om deployment misslyckas:
```bash
heroku logs --tail -a optitech-support-system
```

**DNS fungerar perfekt - du behöver bara deploya koden! 🚀**
