from rest_framework import serializers
from core.models import Country, Category, SKU, SalesData, Channel, Competitor, Vendor

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'code', 'name', 'currency', 'timezone']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'country']

class SKUSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = SKU
        fields = ['id', 'sku_code', 'name', 'brand', 'brand_name', 'category', 
                  'category_name', 'country', 'unit_price', 'pack_size']

class SalesDataSerializer(serializers.ModelSerializer):
    sku_name = serializers.CharField(source='sku.name', read_only=True)
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    country_name = serializers.CharField(source='country.name', read_only=True)
    
    class Meta:
        model = SalesData
        fields = ['id', 'sku', 'sku_name', 'channel', 'channel_name', 'country', 
                  'country_name', 'date', 'quantity_sold', 'revenue', 'unit_price_realized']

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'channel_type', 'country']

class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = ['id', 'name', 'country', 'website', 'market_share']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'country', 'category', 'contact_person', 
                  'email', 'phone', 'rating']

class DashboardSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_quantity = serializers.IntegerField()
    total_skus = serializers.IntegerField()
    timestamp = serializers.DateTimeField()

class SKUPerformanceSerializer(serializers.Serializer):
    sku_code = serializers.CharField()
    sku_name = serializers.CharField()
    brand_name = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    avg_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class ChannelPerformanceSerializer(serializers.Serializer):
    channel_name = serializers.CharField()
    channel_type = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)

class PricingIntelligenceSerializer(serializers.Serializer):
    sku = serializers.CharField()
    our_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    avg_competitor_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    price_position_percent = serializers.FloatField()
    date = serializers.DateField()

class ConsumerInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerInsight
        fields = ['id', 'country', 'category', 'insight_type', 'title', 
                  'description', 'sentiment_score', 'date_collected', 'source']

class CategoryGapSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryGap
        fields = ['id', 'category', 'country', 'gap_description', 'opportunity_score', 
                  'potential_revenue', 'recommended_action', 'identified_date']

class MarketActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketActivity
        fields = ['id', 'activity_type', 'country', 'category', 'brand', 'title', 
                  'description', 'start_date', 'end_date', 'budget', 'roi']
