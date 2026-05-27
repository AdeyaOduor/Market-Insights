from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Country(models.Model):
    COUNTRY_CHOICES = [
        ('RW', 'Rwanda'),
        ('UG', 'Uganda'),
        ('KE', 'Kenya'),
    ]
    
    code = models.CharField(max_length=2, choices=COUNTRY_CHOICES, unique=True)
    name = models.CharField(max_length=50)
    currency = models.CharField(max_length=3)
    timezone = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='categories')
    
    def __str__(self):
        return f"{self.name} - {self.country.name}"

class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brands')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class SKU(models.Model):
    sku_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='skus')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    pack_size = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.sku_code} - {self.name}"

class Channel(models.Model):
    CHANNEL_TYPES = [
        ('MODERN_TRADE', 'Modern Trade'),
        ('TRADITIONAL_TRADE', 'Traditional Trade'),
        ('E_COMMERCE', 'E-commerce'),
        ('WHOLESALE', 'Wholesale'),
    ]
    
    name = models.CharField(max_length=100)
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPES)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} ({self.channel_type})"

class SalesData(models.Model):
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    date = models.DateField()
    quantity_sold = models.IntegerField()
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price_realized = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['sku', 'channel', 'country', 'date']
    
    def __str__(self):
        return f"{self.sku.sku_code} - {self.date} - {self.quantity_sold}"

class Competitor(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    market_share = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    def __str__(self):
        return self.name

class CompetitorProduct(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.competitor.name} - {self.name}"

class PricingHistory(models.Model):
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField()
    promotion_active = models.BooleanField(default=False)
    promotion_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-effective_date']

class ConsumerInsight(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    insight_type = models.CharField(max_length=100)  # e.g., 'preference', 'behavior', 'trend'
    title = models.CharField(max_length=200)
    description = models.TextField()
    sentiment_score = models.FloatField(null=True, blank=True)
    date_collected = models.DateField()
    source = models.CharField(max_length=100)  # e.g., 'survey', 'social_media', 'sales_data'
    
    def __str__(self):
        return f"{self.title} - {self.country.name}"

class MarketActivity(models.Model):
    ACTIVITY_TYPES = [
        ('PROMOTION', 'Promotion'),
        ('CAMPAIGN', 'Marketing Campaign'),
        ('TRADE_ACTIVITY', 'Trade Activity'),
        ('LAUNCH', 'Product Launch'),
    ]
    
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    roi = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.country.name}"

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    
    def __str__(self):
        return self.name

class CategoryGap(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    gap_description = models.TextField()
    opportunity_score = models.IntegerField()  # 1-100
    potential_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    recommended_action = models.TextField()
    identified_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Gap in {self.category.name} - {self.country.name}"