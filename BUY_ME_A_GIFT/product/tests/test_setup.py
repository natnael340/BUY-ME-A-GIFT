from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):
    self.products_url = reverse('products')
    self.product_add_url = reverse('product_create')