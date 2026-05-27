from rest_framework import serializers
from core.models import *

class SKUPerformanceSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='sku.brand.name')
    category_name = serializers.CharField(source='sku.category.name')
    
    class Meta:
        model = SalesData
        fields = ['sku_code', 'sku_name', 'brand_name', 'category_name', 
                  'quantity_sold', 'revenue', 'date']

class ChannelPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['name', 'channel_type', 'country']

class TrendAnalysisSerializer(serializers.Serializer):
    period = serializers.DateField()
    country = serializers.CharField()
    category = serializers.CharField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    growth_rate = serializers.FloatField()

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryGap
        fields = '__all__'