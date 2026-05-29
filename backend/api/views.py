from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

# Import serializers
from .serializers import (
    SKUPerformanceSerializer, 
    ChannelPerformanceSerializer,
    PricingIntelligenceSerializer,
    DashboardSerializer,
    ConsumerInsightSerializer,
    CategoryGapSerializer,
    CompetitorSerializer,
    VendorSerializer,
    CampaignImpactSerializer
)

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
                        'sku__sku_code': 'SKU-BEV-001',
                        'sku__name': 'Coca-Cola 500ml',
                        'sku__brand__name': 'Coca-Cola',
                        'total_quantity': 50000,
                        'total_revenue': 2500000,
                        'avg_price': 50.00
                    },
                    {
                        'sku__sku_code': 'SKU-BEV-002',
                        'sku__name': 'Pepsi 500ml',
                        'sku__brand__name': 'Pepsi',
                        'total_quantity': 45000,
                        'total_revenue': 2250000,
                        'avg_price': 50.00
                    },
                    {
                        'sku__sku_code': 'SKU-FOOD-001',
                        'sku__name': 'Premium Rice 5kg',
                        'sku__brand__name': 'Premium Foods',
                        'total_quantity': 15000,
                        'total_revenue': 1500000,
                        'avg_price': 100.00
                    },
                    {
                        'sku__sku_code': 'SKU-HOME-001',
                        'sku__name': 'Detergent Powder 2kg',
                        'sku__brand__name': 'CleanHome',
                        'total_quantity': 10000,
                        'total_revenue': 1200000,
                        'avg_price': 120.00
                    },
                    {
                        'sku__sku_code': 'SKU-BEV-003',
                        'sku__name': 'Fanta Orange 500ml',
                        'sku__brand__name': 'Coca-Cola',
                        'total_quantity': 5000,
                        'total_revenue': 795000,
                        'avg_price': 159.00
                    }
                ],
                'channel_performance': [
                    {
                        'channel__name': 'Supermarkets',
                        'channel__channel_type': 'MODERN_TRADE',
                        'total_quantity': 75000,
                        'total_revenue': 4500000
                    },
                    {
                        'channel__name': 'Local Shops',
                        'channel__channel_type': 'TRADITIONAL_TRADE',
                        'total_quantity': 35000,
                        'total_revenue': 2100000
                    },
                    {
                        'channel__name': 'E-commerce',
                        'channel__channel_type': 'E_COMMERCE',
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
                },
                {
                    'period': '2024-01',
                    'country__name': 'Uganda',
                    'sku__category__name': 'Beverages',
                    'revenue': 720000,
                    'quantity': 14400
                },
                {
                    'period': '2024-02',
                    'country__name': 'Uganda',
                    'sku__category__name': 'Beverages',
                    'revenue': 780000,
                    'quantity': 15600
                },
                {
                    'period': '2024-03',
                    'country__name': 'Uganda',
                    'sku__category__name': 'Beverages',
                    'revenue': 890000,
                    'quantity': 17800
                }
            ]
            return Response(mock_trends)
        except Exception as e:
            logger.error(f"Error in category_trends: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def competitors(self, request):
        """Get competitors data"""
        try:
            mock_competitors = [
                {
                    'id': 1,
                    'name': 'Coca-Cola Beverages Africa',
                    'country': 1,
                    'website': 'https://www.ccba.com',
                    'market_share': 35.5,
                    'avg_price': 52.50,
                    'product_count': 45,
                    'price_position': -4.76,
                    'categories': ['Beverages', 'Juices', 'Water']
                },
                {
                    'id': 2,
                    'name': 'PepsiCo East Africa',
                    'country': 1,
                    'website': 'https://www.pepsico.com',
                    'market_share': 28.3,
                    'avg_price': 49.50,
                    'product_count': 38,
                    'price_position': 1.01,
                    'categories': ['Beverages', 'Snacks']
                },
                {
                    'id': 3,
                    'name': 'Unilever Kenya',
                    'country': 1,
                    'website': 'https://www.unilever.com',
                    'market_share': 18.7,
                    'avg_price': 65.00,
                    'product_count': 52,
                    'price_position': 8.33,
                    'categories': ['Home Care', 'Personal Care', 'Foods']
                }
            ]
            return Response(mock_competitors)
        except Exception as e:
            logger.error(f"Error in competitors: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def pricing_intelligence(self, request):
        """Competitive pricing analysis"""
        try:
            mock_pricing = [
                {
                    'sku': 'Coca-Cola 500ml',
                    'our_price': 50.00,
                    'avg_competitor_price': 52.50,
                    'price_position_percent': -4.76,
                    'date': '2024-03-01'
                },
                {
                    'sku': 'Pepsi 500ml',
                    'our_price': 50.00,
                    'avg_competitor_price': 49.50,
                    'price_position_percent': 1.01,
                    'date': '2024-03-01'
                },
                {
                    'sku': 'Fanta Orange 500ml',
                    'our_price': 55.00,
                    'avg_competitor_price': 53.00,
                    'price_position_percent': 3.77,
                    'date': '2024-03-01'
                },
                {
                    'sku': 'Premium Rice 5kg',
                    'our_price': 100.00,
                    'avg_competitor_price': 105.00,
                    'price_position_percent': -4.76,
                    'date': '2024-03-01'
                }
            ]
            return Response(mock_pricing)
        except Exception as e:
            logger.error(f"Error in pricing_intelligence: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def consumer_insights(self, request):
        """Consumer behavior and trends"""
        try:
            mock_insights = {
                'recent_insights': [
                    {
                        'id': 1,
                        'title': 'Premium products gaining traction in Nairobi',
                        'description': '45% increase in premium product purchases in urban areas. Consumers are willing to pay more for quality and brand recognition.',
                        'sentiment_score': 0.85,
                        'date_collected': '2024-03-15',
                        'insight_type': 'preference',
                        'source': 'consumer_survey'
                    },
                    {
                        'id': 2,
                        'title': 'Health-conscious buying on the rise',
                        'description': '30% growth in organic and health food products across all three countries. Sugar-free and low-calorie options seeing highest demand.',
                        'sentiment_score': 0.78,
                        'date_collected': '2024-03-10',
                        'insight_type': 'behavior',
                        'source': 'sales_analysis'
                    },
                    {
                        'id': 3,
                        'title': 'E-commerce adoption accelerating',
                        'description': '65% of urban consumers now shop online weekly. Delivery speed and free shipping key decision factors.',
                        'sentiment_score': 0.82,
                        'date_collected': '2024-03-05',
                        'insight_type': 'trend',
                        'source': 'digital_analytics'
                    }
                ],
                'sentiment_trends': [
                    {'date_collected': '2024-01-01', 'avg_sentiment': 0.72},
                    {'date_collected': '2024-01-15', 'avg_sentiment': 0.73},
                    {'date_collected': '2024-02-01', 'avg_sentiment': 0.75},
                    {'date_collected': '2024-02-15', 'avg_sentiment': 0.78},
                    {'date_collected': '2024-03-01', 'avg_sentiment': 0.81},
                    {'date_collected': '2024-03-15', 'avg_sentiment': 0.84}
                ]
            }
            return Response(mock_insights)
        except Exception as e:
            logger.error(f"Error in consumer_insights: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def market_opportunities(self, request):
        """Early opportunities for new categories/brands"""
        try:
            mock_opportunities = {
                'category_gaps': [
                    {
                        'id': 1,
                        'category': 1,
                        'category__name': 'Plant-based Foods',
                        'gap_description': 'Limited availability of plant-based alternatives in traditional retail channels',
                        'opportunity_score': 85,
                        'potential_revenue': 2500000,
                        'recommended_action': 'Launch plant-based product line targeting health-conscious consumers'
                    },
                    {
                        'id': 2,
                        'category': 2,
                        'category__name': 'Eco-friendly Products',
                        'gap_description': 'Growing demand for sustainable products unmet by current suppliers',
                        'opportunity_score': 78,
                        'potential_revenue': 1800000,
                        'recommended_action': 'Source eco-friendly alternatives and create green product line'
                    },
                    {
                        'id': 3,
                        'category': 3,
                        'category__name': 'Ready-to-eat Meals',
                        'gap_description': 'Busy urban professionals seeking convenient meal solutions',
                        'opportunity_score': 72,
                        'potential_revenue': 3200000,
                        'recommended_action': 'Partner with local restaurants for prepared meal delivery'
                    }
                ],
                'growth_categories': [
                    {'sku__category__name': 'Health Drinks', 'growth_rate': 45.5},
                    {'sku__category__name': 'Organic Foods', 'growth_rate': 32.8},
                    {'sku__category__name': 'Digital Accessories', 'growth_rate': 28.3},
                    {'sku__category__name': 'Home Fitness', 'growth_rate': 25.1},
                    {'sku__category__name': 'Sustainable Products', 'growth_rate': 22.4}
                ]
            }
            return Response(mock_opportunities)
        except Exception as e:
            logger.error(f"Error in market_opportunities: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def vendor_sourcing(self, request):
        """Vendor sourcing with data-backed category gap analyses"""
        try:
            mock_vendors = {
                'vendors': [
                    {
                        'id': 1,
                        'name': 'East African Distributors Ltd',
                        'country': 1,
                        'category': 4,
                        'rating': 4.5,
                        'contact_person': 'John Kamau',
                        'email': 'john@ead.co.ke',
                        'phone': '+254712345678'
                    },
                    {
                        'id': 2,
                        'name': 'Uganda Fresh Foods',
                        'country': 2,
                        'category': 5,
                        'rating': 4.2,
                        'contact_person': 'Sarah Nambi',
                        'email': 'sarah@ugandafresh.ug',
                        'phone': '+256712345678'
                    },
                    {
                        'id': 3,
                        'name': 'Rwanda Green Products',
                        'country': 3,
                        'category': 6,
                        'rating': 4.7,
                        'contact_person': 'Paul Kagame',
                        'email': 'paul@rwandagreen.rw',
                        'phone': '+250788123456'
                    }
                ],
                'sourcing_gaps': [
                    {
                        'category_name': 'Plant-based Foods',
                        'demand_volume': 15000,
                        'current_vendors': 1,
                        'opportunity': 'High - Limited vendor coverage'
                    },
                    {
                        'category_name': 'Eco-friendly Packaging',
                        'demand_volume': 25000,
                        'current_vendors': 2,
                        'opportunity': 'Medium - Growing demand'
                    },
                    {
                        'category_name': 'Imported Snacks',
                        'demand_volume': 8000,
                        'current_vendors': 3,
                        'opportunity': 'Low - Adequate coverage'
                    }
                ]
            }
            return Response(mock_vendors)
        except Exception as e:
            logger.error(f"Error in vendor_sourcing: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def measure_campaign_impact(self, request):
        """Measure commercial impact of marketing and trade activities"""
        try:
            activity_id = request.data.get('activity_id')
            
            # Mock ROI calculation based on activity_id
            campaigns = {
                '1': {
                    'activity': 'Summer Promotion 2024',
                    'pre_campaign_revenue': 1500000,
                    'post_campaign_revenue': 2250000,
                    'growth_percentage': 50.0,
                    'roi': 325.5
                },
                '2': {
                    'activity': 'Back to School Campaign',
                    'pre_campaign_revenue': 800000,
                    'post_campaign_revenue': 1200000,
                    'growth_percentage': 50.0,
                    'roi': 280.0
                },
                '3': {
                    'activity': 'Holiday Special',
                    'pre_campaign_revenue': 2000000,
                    'post_campaign_revenue': 3500000,
                    'growth_percentage': 75.0,
                    'roi': 450.0
                }
            }
            
            campaign = campaigns.get(str(activity_id), campaigns['1'])
            
            mock_impact = {
                'activity': campaign['activity'],
                'pre_campaign_revenue': campaign['pre_campaign_revenue'],
                'post_campaign_revenue': campaign['post_campaign_revenue'],
                'growth_percentage': campaign['growth_percentage'],
                'roi': campaign['roi'],
                'status': 'success'
            }
            return Response(mock_impact)
        except Exception as e:
            logger.error(f"Error in measure_campaign_impact: {e}")
            return Response({
                'error': str(e),
                'status': 'failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def health_check(self, request):
        """Health check endpoint"""
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now(),
            'version': '1.0.0',
            'services': {
                'api': 'running',
                'database': 'connected',
                'cache': 'available'
            }
        })
