import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_insights.settings')
app = Celery('market_insights')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
