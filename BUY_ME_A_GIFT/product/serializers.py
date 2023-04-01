from rest_framework import serializers
from .models import Product, ProductCategory, WishList

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
class ProductCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name']

class ProductCreateSerializer(serializers.ModelSerializer):
    product_category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())
    class Meta: 
        model = Product
        fields = ['id', 'name', 'price', 'rank', 'created_time', 'updated_time', 'product_category']

class ProductListSerializer(serializers.ModelSerializer):
    product_category = ProductCategoryCreateSerializer()
    class Meta:
        model = Product
        fields = ['id','name', 'price', 'created_time', 'product_category']

class WishListSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)

    class Meta:
        model = WishList
        fields = '__all__'
class WishListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = WishList
        fields = ''