#!/bin/bash

echo "🚀 Setting up IssueHub Backend..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and update DATABASE_URL and SECRET_KEY"
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate || venv\Scripts\activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Create PostgreSQL database: createdb issuehub"
echo "3. Run migrations: alembic upgrade head"
echo "4. (Optional) Seed demo data: python app/seed.py"
echo "5. Start server: uvicorn app.main:app --reload"
