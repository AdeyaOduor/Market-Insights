from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Q, F
from django.db.models.functions import TruncMonth, TruncWeek
from django.utils import timezone
from datetime import timedelta
import pandas as pd
import numpy as np

from core.models import *
from .serializers import *
from .dashboard_serializers import *

class DashboardViewSet(viewsets.GenericViewSet):
    
    @action(detail=False, methods=['get'])
    def unified_dashboard(self, request):
        """Consolidated dashboard with channel and SKU-level performance"""
        country_code = request.query_params.get('country')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        # Filter sales data
        sales_data = SalesData.objects.all()
        if country_code:
            sales_data = sales_data.filter(country__code=country_code)
        if date_from and date_to:
            sales_data = sales_data.filter(date__range=[date_from, date_to])
        
        # SKU-level performance
        sku_performance = sales_data.values(
            'sku__sku_code', 'sku__name', 'sku__brand__name'
        ).annotate(
            total_quantity=Sum('quantity_sold'),
            total_revenue=Sum('revenue'),
            avg_price=Avg('unit_price_realized')
        )
        
        # Channel-level performance
        channel_performance = sales_data.values(
            'channel__name', 'channel__channel_type'
        ).annotate(
            total_quantity=Sum('quantity_sold'),
            total_revenue=Sum('revenue')
        )
        
        # Country comparison
        country_performance = sales_data.values('country__name').annotate(
            total_revenue=Sum('revenue'),
            total_quantity=Sum('quantity_sold')
        )
        
        return Response({
            'sku_performance': sku_performance,
            'channel_performance': channel_performance,
            'country_comparison': country_performance,
            'timestamp': timezone.now()
        })
    
    @action(detail=False, methods=['get'])
    def category_trends(self, request):
        """Category trends across all three countries"""
        category_id = request.query_params.get('category')
        period = request.query_params.get('period', 'monthly')  # weekly, monthly, quarterly
        
        sales_data = SalesData.objects.filter(category_id=category_id) if category_id else SalesData.objects.all()
        
        if period == 'monthly':
            trends = sales_data.annotate(
                period=TruncMonth('date')
            ).values('period', 'country__name', 'sku__category__name').annotate(
                revenue=Sum('revenue'),
                quantity=Sum('quantity_sold')
            ).order_by('period')
        else:
            trends = sales_data.annotate(
                period=TruncWeek('date')
            ).values('period', 'country__name', 'sku__category__name').annotate(
                revenue=Sum('revenue'),
                quantity=Sum('quantity_sold')
            ).order_by('period')
        
        return Response(trends)
    
    @action(detail=False, methods=['get'])
    def pricing_intelligence(self, request):
        """Competitive pricing analysis"""
        country_code = request.query_params.get('country')
        category_id = request.query_params.get('category')
        
        # Get our pricing
        our_pricing = PricingHistory.objects.select_related('sku')
        if country_code:
            our_pricing = our_pricing.filter(sku__country__code=country_code)
        if category_id:
            our_pricing = our_pricing.filter(sku__category_id=category_id)
        
        # Get competitor pricing
        competitor_pricing = CompetitorProduct.objects.select_related('competitor')
        if country_code:
            competitor_pricing = competitor_pricing.filter(country__code=country_code)
        if category_id:
            competitor_pricing = competitor_pricing.filter(category_id=category_id)
        
        # Calculate price positioning
        price_analysis = []
        for our_price in our_pricing[:50]:  # Limit for performance
            comp_prices = competitor_pricing.filter(
                category=our_price.sku.category
            ).values_list('price', flat=True)
            
            if comp_prices:
                avg_comp_price = np.mean(comp_prices)
                price_position = ((our_price.price - avg_comp_price) / avg_comp_price) * 100
            else:
                avg_comp_price = None
                price_position = None
            
            price_analysis.append({
                'sku': our_price.sku.sku_code,
                'our_price': our_price.price,
                'avg_competitor_price': avg_comp_price,
                'price_position_percent': price_position,
                'date': our_price.effective_date
            })
        
        return Response(price_analysis)
    
    @action(detail=False, methods=['get'])
    def consumer_insights(self, request):
        """Consumer behavior and trends"""
        country_code = request.query_params.get('country')
        category_id = request.query_params.get('category')
        
        insights = ConsumerInsight.objects.all()
        if country_code:
            insights = insights.filter(country__code=country_code)
        if category_id:
            insights = insights.filter(category_id=category_id)
        
        # Get sentiment trends
        sentiment_trends = insights.values('date_collected').annotate(
            avg_sentiment=Avg('sentiment_score')
        ).order_by('date_collected')
        
        # Get top insights by category
        top_insights = insights.order_by('-date_collected')[:20]
        
        return Response({
            'recent_insights': ConsumerInsightSerializer(top_insights, many=True).data,
            'sentiment_trends': sentiment_trends
        })
    
    @action(detail=False, methods=['get'])
    def market_opportunities(self, request):
        """Early opportunities for new categories/brands"""
        country_code = request.query_params.get('country')
        
        gaps = CategoryGap.objects.all()
        if country_code:
            gaps = gaps.filter(country__code=country_code)
        
        # Score and rank opportunities
        opportunities = gaps.annotate(
            priority_score=F('opportunity_score') * (F('potential_revenue') / 1000000)
        ).order_by('-priority_score')
        
        # Identify high-growth categories
        six_months_ago = timezone.now().date() - timedelta(days=180)
        growth_categories = SalesData.objects.filter(
            date__gte=six_months_ago
        ).values('sku__category__name', 'country__name').annotate(
            growth_rate=((Sum('revenue') - Avg('revenue')) / Avg('revenue')) * 100
        ).order_by('-growth_rate')
        
        return Response({
            'category_gaps': CategoryGapSerializer(opportunities, many=True).data,
            'growth_categories': growth_categories
        })
    
    @action(detail=False, methods=['get'])
    def vendor_sourcing(self, request):
        """Vendor sourcing with data-backed category gap analyses"""
        country_code = request.query_params.get('country')
        category_id = request.query_params.get('category')
        
        vendors = Vendor.objects.all()
        if country_code:
            vendors = vendors.filter(country__code=country_code)
        if category_id:
            vendors = vendors.filter(category_id=category_id)
        
        # Find gaps where current supply doesn't meet demand
        high_demand_categories = SalesData.objects.values(
            'sku__category_id', 'country_id'
        ).annotate(
            total_demand=Sum('quantity_sold')
        ).order_by('-total_demand')
        
        vendor_coverage = []
        for demand in high_demand_categories[:10]:
            vendor_count = Vendor.objects.filter(
                category_id=demand['sku__category_id'],
                country_id=demand['country_id']
            ).count()
            
            if vendor_count < 3:  # Less than 3 vendors indicates a gap
                vendor_coverage.append({
                    'category_id': demand['sku__category_id'],
                    'category_name': Category.objects.get(id=demand['sku__category_id']).name,
                    'demand_volume': demand['total_demand'],
                    'current_vendors': vendor_count,
                    'opportunity': 'High - Limited vendor coverage'
                })
        
        return Response({
            'vendors': VendorSerializer(vendors, many=True).data,
            'sourcing_gaps': vendor_coverage
        })
    
    @action(detail=False, methods=['post'])
    def measure_campaign_impact(self, request):
        """Measure commercial impact of marketing and trade activities"""
        activity_id = request.data.get('activity_id')
        
        activity = MarketActivity.objects.get(id=activity_id)
        
        # Get sales before campaign
        before_sales = SalesData.objects.filter(
            date__range=[activity.start_date - timedelta(days=30), activity.start_date - timedelta(days=1)]
        )
        
        if activity.brand:
            before_sales = before_sales.filter(sku__brand=activity.brand)
        if activity.category:
            before_sales = before_sales.filter(sku__category=activity.category)
        
        # Get sales after campaign
        after_sales = SalesData.objects.filter(
            date__range=[activity.end_date + timedelta(days=1), activity.end_date + timedelta(days=30)]
        )
        
        if activity.brand:
            after_sales = after_sales.filter(sku__brand=activity.brand)
        if activity.category:
            after_sales = after_sales.filter(sku__category=activity.category)
        
        before_total = before_sales.aggregate(total=Sum('revenue'))['total'] or 0
        after_total = after_sales.aggregate(total=Sum('revenue'))['total'] or 0
        
        if before_total > 0:
            growth_percentage = ((after_total - before_total) / before_total) * 100
        else:
            growth_percentage = 0
        
        # Calculate ROI
        if activity.budget and activity.budget > 0:
            roi = ((after_total - before_total - activity.budget) / activity.budget) * 100
        else:
            roi = None
        
        # Update activity with calculated ROI
        activity.roi = roi
        activity.save()
        
        return Response({
            'activity': activity.title,
            'pre_campaign_revenue': before_total,
            'post_campaign_revenue': after_total,
            'growth_percentage': growth_percentage,
            'roi': roi,
            'status': 'success'
        })