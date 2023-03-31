from django.db import models
# from User.models import User

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='category_owner')


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    rank = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    updated_time = models.DateTimeField(auto_now=True)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name='product_category')
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='owner')

class WishList(models.Model):
    user = models.OneToOneField(
        'user.User', on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField(
        Product, related_name='whishlist_products', blank=True)

    def save(self, *args, **kwargs):
        categories = set()
        products = []
        for product in self.products.all():
            if product.product_category in categories:
                continue
            categories.add(product.product_category)
            products.append(product)
        self.products.set(products)
        super(WishList, self).save(*args, **kwargs)
