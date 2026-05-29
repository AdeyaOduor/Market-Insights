# api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

# Try to import models, handle if they don't exist yet
try:
    from core.models import Country, Category, SKU, SalesData, Channel, Competitor, Vendor
    from .serializers import (
        SKUPerformanceSerializer, ChannelPerformanceSerializer, 
        PricingIntelligenceSerializer, DashboardSerializer
    )
except ImportError as e:
    logger.warning(f"Models not yet created: {e}")
    # Define dummy classes if models don't exist
    Country = None
    Category = None
    SKU = None
    SalesData = None

class DashboardViewSet(viewsets.GenericViewSet):
    
    @action(detail=False, methods=['get'])
    def unified_dashboard(self, request):
        """Consolidated dashboard with channel and SKU-level performance"""
        try:
            # Mock data for initial setup
            mock_data = {
                'total_revenue': 8245000,
                'total_quantity': 125000,
                'total_skus': 2450,
                'timestamp': timezone.now(),
                'sku_performance': [
                    {
                        'sku_code': 'SKU-BEV-001',
                        'sku_name': 'Coca-Cola 500ml',
                        'brand_name': 'Coca-Cola',
                        'total_quantity': 50000,
                        'total_revenue': 2500000,
                        'avg_price': 50.00
                    },
                    {
                        'sku_code': 'SKU-BEV-002',
                        'sku_name': 'Pepsi 500ml',
                        'brand_name': 'Pepsi',
                        'total_quantity': 45000,
                        'total_revenue': 2250000,
                        'avg_price': 50.00
                    },
                    {
                        'sku_code': 'SKU-FOOD-001',
                        'sku_name': 'Premium Rice 5kg',
                        'brand_name': 'Premium Foods',
                        'total_quantity': 15000,
                        'total_revenue': 1500000,
                        'avg_price': 100.00
                    }
                ],
                'channel_performance': [
                    {
                        'channel_name': 'Supermarkets',
                        'channel_type': 'MODERN_TRADE',
                        'total_quantity': 75000,
                        'total_revenue': 4500000
                    },
                    {
                        'channel_name': 'Local Shops',
                        'channel_type': 'TRADITIONAL_TRADE',
                        'total_quantity': 35000,
                        'total_revenue': 2100000
                    },
                    {
                        'channel_name': 'E-commerce',
                        'channel_type': 'E_COMMERCE',
                        'total_quantity': 15000,
                        'total_revenue': 1645000
                    }
                ],
                'country_comparison': [
                    {'country__name': 'Kenya', 'total_revenue': 3500000, 'total_quantity': 55000},
                    {'country__name': 'Uganda', 'total_revenue': 2800000, 'total_quantity': 42000},
                    {'country__name': 'Rwanda', 'total_revenue': 1945000, 'total_quantity': 28000}
                ]
            }
            return Response(mock_data)
        except Exception as e:
            logger.error(f"Error in unified_dashboard: {e}")
            return Response({
                'error': 'Unable to fetch dashboard data',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def category_trends(self, request):
        """Category trends across all three countries"""
        try:
            mock_trends = [
                {
                    'period': '2024-01',
                    'country__name': 'Kenya',
                    'sku__category__name': 'Beverages',
                    'revenue': 850000,
                    'quantity': 17000
                },
                {
                    'period': '2024-02',
                    'country__name': 'Kenya',
                    'sku__category__name': 'Beverages',
                    'revenue': 920000,
                    'quantity': 18400
                },
                {
                    'period': '2024-03',
                    'country__name': 'Kenya',
                    'sku__category__name': 'Beverages',
                    'revenue': 1050000,
                    'quantity': 21000
                }
            ]
            return Response(mock_trends)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def pricing_intelligence(self, request):
        """Competitive pricing analysis"""
        try:
            mock_pricing = [
                {
                    'sku': 'SKU-BEV-001',
                    'our_price': 50.00,
                    'avg_competitor_price': 52.50,
                    'price_position_percent': -4.76,
                    'date': '2024-03-01'
                },
                {
                    'sku': 'SKU-BEV-002',
                    'our_price': 50.00,
                    'avg_competitor_price': 49.50,
                    'price_position_percent': 1.01,
                    'date': '2024-03-01'
                }
            ]
            return Response(mock_pricing)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def consumer_insights(self, request):
        """Consumer behavior and trends"""
        try:
            mock_insights = {
                'recent_insights': [
                    {
                        'title': 'Premium products gaining traction in Nairobi',
                        'description': '45% increase in premium product purchases in urban areas',
                        'sentiment_score': 0.85,
                        'date_collected': '2024-03-15'
                    },
                    {
                        'title': 'Health-conscious buying on the rise',
                        'description': '30% growth in organic and health food products',
                        'sentiment_score': 0.78,
                        'date_collected': '2024-03-10'
                    }
                ],
                'sentiment_trends': [
                    {'date_collected': '2024-01-01', 'avg_sentiment': 0.72},
                    {'date_collected': '2024-02-01', 'avg_sentiment': 0.75},
                    {'date_collected': '2024-03-01', 'avg_sentiment': 0.81}
                ]
            }
            return Response(mock_insights)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def market_opportunities(self, request):
        """Early opportunities for new categories/brands"""
        try:
            mock_opportunities = {
                'category_gaps': [
                    {
                        'category__name': 'Plant-based Foods',
                        'gap_description': 'Limited availability of plant-based alternatives',
                        'opportunity_score': 85,
                        'potential_revenue': 2500000,
                        'recommended_action': 'Launch plant-based product line'
                    },
                    {
                        'category__name': 'Eco-friendly Products',
                        'gap_description': 'Growing demand for sustainable products unmet',
                        'opportunity_score': 78,
                        'potential_revenue': 1800000,
                        'recommended_action': 'Source eco-friendly alternatives'
                    }
                ],
                'growth_categories': [
                    {'sku__category__name': 'Health Drinks', 'growth_rate': 45.5},
                    {'sku__category__name': 'Organic Foods', 'growth_rate': 32.8},
                    {'sku__category__name': 'Digital Accessories', 'growth_rate': 28.3}
                ]
            }
            return Response(mock_opportunities)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def vendor_sourcing(self, request):
        """Vendor sourcing with data-backed category gap analyses"""
        try:
            mock_vendors = {
                'vendors': [
                    {
                        'name': 'East African Distributors Ltd',
                        'country': 'Kenya',
                        'category': 'Beverages',
                        'rating': 4.5,
                        'contact_person': 'John Kamau'
                    },
                    {
                        'name': 'Uganda Fresh Foods',
                        'country': 'Uganda',
                        'category': 'Food Products',
                        'rating': 4.2,
                        'contact_person': 'Sarah Nambi'
                    }
                ],
                'sourcing_gaps': [
                    {
                        'category_name': 'Plant-based Foods',
                        'demand_volume': 15000,
                        'current_vendors': 1,
                        'opportunity': 'High - Limited vendor coverage'
                    }
                ]
            }
            return Response(mock_vendors)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def measure_campaign_impact(self, request):
        """Measure commercial impact of marketing and trade activities"""
        try:
            activity_id = request.data.get('activity_id')
            
            # Mock ROI calculation
            mock_impact = {
                'activity': 'Summer Promotion 2024',
                'pre_campaign_revenue': 1500000,
                'post_campaign_revenue': 2250000,
                'growth_percentage': 50.0,
                'roi': 325.5,
                'status': 'success'
            }
            return Response(mock_impact)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def health_check(self, request):
        """Health check endpoint"""
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now(),
            'version': '1.0.0'
        })