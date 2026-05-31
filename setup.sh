#!/bin/bash
# ─── Asari Florist — Setup Script ───
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗄️  Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "🔑 Create superuser (admin login)..."
python manage.py createsuperuser

echo "🌱 Loading initial data..."
python manage.py seed_data 2>/dev/null || echo "  (seed_data command not found — skip)"

echo ""
echo "✅ Setup complete!"
echo "🚀 Start server with: python manage.py runserver"
echo "🌐 Open: http://127.0.0.1:8000"
echo "🔐 Admin: http://127.0.0.1:8000/admin-panel/login/"
