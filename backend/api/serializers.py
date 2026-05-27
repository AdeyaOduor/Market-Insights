from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_quantity = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
