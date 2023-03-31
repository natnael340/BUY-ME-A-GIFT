from django.db import models

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    rank = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    updated_time = models.DateTimeField(auto_now=True)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name='product_category')
