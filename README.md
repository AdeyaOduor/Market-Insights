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

adeya
adeyadavid@gmail.com
P@ssw0rd 1980