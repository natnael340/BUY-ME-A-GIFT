from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from Product.models import Product
import uuid

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('Email', unique=True)
    is_active = models.BooleanField('IsActive', default=True)
    is_admin = models.BooleanField('IsAdmin', default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class WishList(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField(
        'product.Product', related_name='whishlist_products')

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
