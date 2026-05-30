# Market-Insights

cd backend
source venv/bin/activate

sudo -u postgres psql
postgres=# sudo systemctl start postgresql
postgres-# sudo systemctl enable postgresql
CREATE DATABASE market_insights;
CREATE USER postgres WITH PASSWORD 'postgres123';

# Test PostgreSQL connection
PGPASSWORD=postgres123 psql -h localhost -U postgres -d market_insights -c "SELECT 1;"

pip install dj-database-url

# If successful, run Django commands
python3 manage.py check --database default

# Make migrations
python3 manage.py makemigrations

# Create initial migrations for apps
python3 manage.py makemigrations core
python3 manage.py makemigrations api

# Apply migrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser

adeya
adeyadavid@gmail.com
P@ssw0rd 1980

python3 manage.py runserver

Django version 5.2.14, using settings 'market_insights.settings'
Starting development server at http://127.0.0.1:8000/adeya
Quit the server with CONTROL-C.