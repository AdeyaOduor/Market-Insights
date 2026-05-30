from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.http import JsonResponse
from . import views

router = DefaultRouter()
router.register(r'dashboard', views.DashboardViewSet, basename='dashboard')

def api_index(request):
    """API index page"""
    return JsonResponse({
        'message': 'Market Insights Platform API',
        'version': '1.0.0',
        'endpoints': {
            'dashboard': '/api/dashboard/',
            'available_actions': [
                '/api/dashboard/unified_dashboard/',
                '/api/dashboard/category_trends/',
                '/api/dashboard/pricing_intelligence/',
                '/api/dashboard/consumer_insights/',
                '/api/dashboard/market_opportunities/',
                '/api/dashboard/vendor_sourcing/',
                '/api/dashboard/competitors/',
                '/api/dashboard/health_check/',
            ]
        }
    })

urlpatterns = [
    path('', api_index, name='api_index'),
    path('', include(router.urls)),
]
