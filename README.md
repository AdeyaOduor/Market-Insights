# Market-Insights

cd backend

#### On Linux: 
source venv/bin/activate 
#### On Windows: 
venv\Scripts\activate

pip install -r requirements.txt

sudo -u postgres psql
postgres=# sudo systemctl start postgresql
postgres-# sudo systemctl enable postgresql
CREATE DATABASE market_insights;
CREATE USER postgres WITH PASSWORD 'postgres123';

### Test PostgreSQL connection
PGPASSWORD=postgres123 psql -h localhost -U postgres -d market_insights -c "SELECT 1;"

pip install dj-database-url

### If successful, run Django commands
python3 manage.py check --database default

### Make migrations
python3 manage.py makemigrations

### Create initial migrations for apps
python3 manage.py makemigrations core
python3 manage.py makemigrations api

### Apply migrations
python3 manage.py migrate

### Create superuser
python3 manage.py createsuperuser

adeya
adeyadavid@gmail.com
P@ssw0rd 1980

python3 manage.py runserver

Django version 5.2.14, using settings 'market_insights.settings'
Starting development server at http://127.0.0.1:8000/adeya
Quit the server with CONTROL-C.

### Frontend (in new terminal)
cd frontend
npm install
npm start

### Celery (for background tasks)
celery -A market_insights worker -l info

### Set environment variables
export DB_PASSWORD=your_secure_password
export DJANGO_SECRET_KEY=your_secret_key

### Build and deploy with Docker
docker-compose -f docker-compose.yml up -d --build

### Initialize database
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

### Load initial data
docker-compose exec backend python manage.py loaddata initial_data.json

### yaml || CI/CD Pipeline (GitHub Actions example)
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Build and push Docker images
        run: |
          docker-compose build
          docker-compose push
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /app/market-insights-platform
            docker-compose pull
            docker-compose up -d --force-recreate
            docker system prune -f