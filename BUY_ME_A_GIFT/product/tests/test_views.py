from django.test import TestCase, RequestFactory
from django.urls import reverse

from rest_framework import status
from product.models import Product, ProductCategory
from product.views import (
    ProductView,
)
from user.models import User
class ProductViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email="test@example.com", password="123456")
        self.product_category = ProductCategory.objects.create(name="test", owner=self.user)
        self.product = Product.objects.create(
            name='Product',
            price=50.00,
            currency='EUR',
            rank=9,
            owner=self.user,
            product_category = self.product_category,
        )
        

    def test_product_view(self):
        request = self.factory.get(reverse('product', kwargs={'id': self.product.id}))
        response = ProductView.as_view()(request, id=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_product_view_notfound(self):
        request = self.factory.get(reverse('product', kwargs={'id': 1000}))
        response = ProductView.as_view()(request, id=1000)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email="test@example.com", password="123456")
        self.product_category = ProductCategory.objects.create(name="test", owner=self.user)
        
    def test_product_create_view(self):
        request = self.factory.post(reverse('product_create'))
        force_a