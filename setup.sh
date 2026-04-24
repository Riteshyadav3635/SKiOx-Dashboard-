#!/bin/bash
# SkiOx Dashboard Setup Script

echo "======================================"
echo "SkiOx Dashboard Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "Virtual environment created!"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated!"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Dependencies installed!"
echo ""

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Migrations completed!"
echo ""

# Create superuser
echo "Creating superuser..."
echo "Please enter superuser credentials:"
python manage.py createsuperuser
echo ""

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo ""

# Create sample data
echo "Creating sample data..."
python manage.py shell < load_sample_data.py
echo "Sample data loaded!"
echo ""

echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To run the development server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then open your browser to:"
echo "  http://127.0.0.1:8000/"
echo ""
