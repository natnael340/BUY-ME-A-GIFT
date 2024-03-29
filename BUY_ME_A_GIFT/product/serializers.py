from rest_framework import serializers
from .models import Product, ProductCategory, WishList
from typing import Any

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
        fields = ['products']
    def to_representation(self, instance: WishList | None) -> Any:
        if instance is None:
            return {}
        return super().to_representation(instance)
    
class WishListCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField() 
    
    def validate_product_id(self, value: int) -> Product|None:
        try:
            product = Product.objects.get(id=value)
            return product
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product id")
        
    def validate(self, attrs: dict) -> dict:
        user = self.context.get('request').user
        try:
            wishlist = user.wishlist
        except WishList.DoesNotExist:
            wishlist = None

        product = attrs['product_id']
        if wishlist and product.product_category in [p.product_category for p in wishlist.products.all()]:
            raise serializers.ValidationError('You can add only one product from each category to your wishlist')
        
        return attrs
    
    def create(self, validated_data: dict) -> dict:
        user = self.context.get('request').user
        try:
            wishlist = user.wishlist
            print("get")
        except WishList.DoesNotExist:
            wishlist = WishList.objects.create(user=user)
            print("create")
            wishlist.save()
        
        product = validated_data['product_id']
        wishlist.products.add(product)  
        wishlist.save()
        #wishlist.refresh_from_db()
        return {"product_id": product.id}
    
class WishListUnauthorizedSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)

    class Meta:
        model = WishList
        fields = ['products']
    def to_representation(self, instance: WishList | None) -> dict|Any:
        if instance is None:
            return {}
        return super().to_representation(instance)
    