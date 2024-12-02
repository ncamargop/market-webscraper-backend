from rest_framework import serializers
from .models import Product, Index

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "product_name", "price", "quantity", "store", "uploaded_at", "image"] 


class IndexSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = Index
        fields = ["date", "unweighted_index"] 
