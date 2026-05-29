from django.contrib import admin
from .models import (
    Country, Category, Brand, SKU, Channel, SalesData, 
    Competitor, CompetitorProduct, PricingHistory, ConsumerInsight,
    MarketActivity, Vendor, CategoryGap
)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'currency']
    search_fields = ['name', 'code']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'parent']
    list_filter = ['country']
    search_fields = ['name']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'country']
    list_filter = ['country', 'category']
    search_fields = ['name']

@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ['sku_code', 'name', 'brand', 'category', 'country', 'unit_price']
    list_filter = ['country', 'category', 'brand']
    search_fields = ['sku_code', 'name']

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel_type', 'country']
    list_filter = ['country', 'channel_type']

@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ['sku', 'channel', 'country', 'date', 'quantity_sold', 'revenue']
    list_filter = ['country', 'channel', 'date']
    search_fields = ['sku__sku_code']

@admin.register(Competitor)
class CompetitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'market_share']
    list_filter = ['country']

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'category', 'rating']
    list_filter = ['country', 'category']

@admin.register(CategoryGap)
class CategoryGapAdmin(admin.ModelAdmin):
    list_display = ['category', 'country', 'opportunity_score', 'potential_revenue']
    list_filter = ['country']
