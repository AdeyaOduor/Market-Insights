from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view

def home_page(request):
    """Serve the home page"""
    return render(request, 'index.html')

@api_view(['GET'])
def api_root(request):
    """API Root endpoint with available endpoints"""
    return JsonResponse({
        'message': 'Welcome to Market Insights Platform API',
        'version': '1.0.0',
        'endpoints': {
            'web_interface': '/',
            'admin_panel': '/admin/',
            'api_documentation': '/api/',
            'api_endpoints': {
                'dashboard': '/api/dashboard/',
                'auth': {
                    'token_obtain': '/api/token/',
                    'token_refresh': '/api/token/refresh/',
                },
                'available_actions': {
                    'unified_dashboard': '/api/dashboard/unified_dashboard/',
                    'category_trends': '/api/dashboard/category_trends/',
                    'pricing_intelligence': '/api/dashboard/pricing_intelligence/',
                    'consumer_insights': '/api/dashboard/consumer_insights/',
                    'market_opportunities': '/api/dashboard/market_opportunities/',
                    'vendor_sourcing': '/api/dashboard/vendor_sourcing/',
                    'competitors': '/api/dashboard/competitors/',
                    'health_check': '/api/dashboard/health_check/',
                }
            }
        },
        'documentation': 'For more information, visit the admin panel or check the API documentation'
    })

urlpatterns = [
    # Root endpoint - serve HTML page
    path('', home_page, name='home'),
    path('api/root/', api_root, name='api_root'),
    
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/', include('api.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
