from django.test import TestCase, RequestFactory
from django.urls import reverse

from rest_framework import status
from product.models import Product
from product.views import (
    ProductView,
)

class ProductViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.product = Product.objects.create(
            name='Product',
            price=50.00,
            currency='EUR',
            rank=9,
        )

    def test_product_view(self):
        request = self.factory.get(reverse('product', kwargs={'id': self.product.id}))
        response = ProductView.as_view()(request, id=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)