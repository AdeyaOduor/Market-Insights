from rest_framework import serializers

# Define serializers without model dependencies first
# These will work even if models aren't created yet

class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    code = serializers.CharField(max_length=2)
    name = serializers.CharField(max_length=50)
    currency = serializers.CharField(max_length=3, required=False)
    timezone = serializers.CharField(max_length=50, required=False)

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    parent = serializers.IntegerField(required=False, allow_null=True)
    country = serializers.IntegerField()

class BrandSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    category = serializers.IntegerField()
    country = serializers.IntegerField()

class SKUSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    sku_code = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=200)
    brand = serializers.IntegerField(required=False, allow_null=True)
    brand_name = serializers.CharField(required=False)
    category = serializers.IntegerField()
    category_name = serializers.CharField(required=False)
    country = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    pack_size = serializers.CharField(max_length=50, required=False)

class ChannelSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    channel_type = serializers.CharField(max_length=20)
    country = serializers.IntegerField()

class SalesDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    sku = serializers.IntegerField()
    sku_name = serializers.CharField(required=False)
    channel = serializers.IntegerField()
    channel_name = serializers.CharField(required=False)
    country = serializers.IntegerField()
    country_name = serializers.CharField(required=False)
    date = serializers.DateField()
    quantity_sold = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    unit_price_realized = serializers.DecimalField(max_digits=10, decimal_places=2)

class CompetitorSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    country = serializers.IntegerField()
    website = serializers.URLField(required=False)
    market_share = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    avg_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    product_count = serializers.IntegerField(required=False)
    price_position = serializers.FloatField(required=False)
    categories = serializers.ListField(required=False)

class VendorSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    country = serializers.IntegerField()
    category = serializers.IntegerField()
    contact_person = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, allow_null=True)

class DashboardSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_quantity = serializers.IntegerField()
    total_skus = serializers.IntegerField()
    timestamp = serializers.DateTimeField()

class SKUPerformanceSerializer(serializers.Serializer):
    sku__sku_code = serializers.CharField()
    sku__name = serializers.CharField()
    sku__brand__name = serializers.CharField(required=False)
    total_quantity = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    avg_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

class ChannelPerformanceSerializer(serializers.Serializer):
    channel__name = serializers.CharField()
    channel__channel_type = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)

class PricingIntelligenceSerializer(serializers.Serializer):
    sku = serializers.CharField()
    our_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    avg_competitor_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    price_position_percent = serializers.FloatField(required=False, allow_null=True)
    date = serializers.DateField()

class ConsumerInsightSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    country = serializers.IntegerField()
    category = serializers.IntegerField()
    insight_type = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    sentiment_score = serializers.FloatField(required=False, allow_null=True)
    date_collected = serializers.DateField()
    source = serializers.CharField(max_length=100)

class CategoryGapSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    category = serializers.IntegerField()
    category__name = serializers.CharField(required=False)
    country = serializers.IntegerField()
    gap_description = serializers.CharField()
    opportunity_score = serializers.IntegerField()
    potential_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    recommended_action = serializers.CharField()
    identified_date = serializers.DateField(required=False)

class MarketActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    activity_type = serializers.CharField(max_length=20)
    country = serializers.IntegerField()
    category = serializers.IntegerField(required=False, allow_null=True)
    brand = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    budget = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    roi = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)

class OpportunitySerializer(serializers.Serializer):
    category_name = serializers.CharField()
    demand_volume = serializers.IntegerField()
    current_vendors = serializers.IntegerField()
    opportunity = serializers.CharField()

class CampaignImpactSerializer(serializers.Serializer):
    activity = serializers.CharField()
    pre_campaign_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    post_campaign_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    growth_percentage = serializers.FloatField()
    roi = serializers.FloatField(required=False, allow_null=True)
    status = serializers.CharField()
