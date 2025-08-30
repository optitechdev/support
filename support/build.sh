!/bin/bash

# Optitech AI Support System Build Script
echo "🤖 Building Optitech AI Support System..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Verify AI connection
echo "🔗 Testing AI connection..."
python azure_chat_assistant.py

echo ""
echo "🎉 AI Support System is ready!"
echo ""
echo "🚀 To start the AI support chat:"
echo "  source .venv/bin/activate"
echo "  python support_assistant_main.py"
echo ""
echo "💡 How it works:"
echo "  - AI chattar först naturligt med kunden"
echo "  - Hjälper och löser problem direkt om möjligt"
echo "  - Skapar automatiskt supportärende när det behövs"
