# Optitech Support Assistant

En intelligent supportassistent som använder Azure OpenAI för att hantera supportärenden och skicka e-post via SendGrid.

## Funktioner

- 🤖 **AI-driven Supportassistent** - Använder Azure OpenAI GPT-4 för intelligent chattstöd
- 📧 **Automatisk E-posthantering** - Skickar bekräftelser och notifikationer via SendGrid
- 🎫 **Ärendehantering** - Genererar unika ärendenummer och spårar supportärenden
- 🇸🇪 **Svenska språket** - Komplett stöd för svenska användare

## Komponenter

### 1. `azure_chat_assistant.py`

Enkel AI-chatassistent som demonstrerar grundläggande Azure OpenAI-integration.

### 2. `optitech_supportmail.py`

E-postmodul som hanterar utskick av:

- Bekräftelsemail till kunder
- Interna notifikationer till supportteamet

### 3. `support_assistant_main.py`

Huvudapplikationen som kombinerar AI-chat med ärendehantering och e-post.

## Installation och Setup

### 1. Bygg projektet

```bash
./build.sh
```

### 2. Konfigurera miljövariabler

```bash
cp .env.template .env
# Redigera .env med dina API-nycklar
```

### 3. Kör applikationen

```bash
source .venv/bin/activate
python support_assistant_main.py
```

## Krav

- Python 3.12+
- Azure OpenAI API-nyckel
- SendGrid API-nyckel

## Dependencies

- `python-dotenv` - Miljövariabelhantering
- `sendgrid` - E-postutskick
- `requests` - HTTP-förfrågningar till Azure OpenAI

## Användning

1. Starta huvudapplikationen: `python support_assistant_main.py`
2. Följ instruktionerna för att ange namn, e-post och ärendebeskrivning
3. Systemet genererar automatiskt ett ärendenummer och skickar bekräftelsemail

## Miljövariabler

| Variabel | Beskrivning |
|----------|-------------|
| `AZURE_OPENAI_API_KEY` | Din Azure OpenAI API-nyckel |
| `SENDGRID_API_KEY` | Din SendGrid API-nyckel |

## Utveckling

Projektet använder en virtuell miljö för att hantera beroenden. Alla nödvändiga paket finns i `requirements.txt`.
