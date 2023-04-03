from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import force_authenticate
from rest_framework import status
from product.models import Product, ProductCategory
from product.views import (
    ProductView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductListView,
    CategoryCreateView
)
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import json


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
        self.product_category2 = ProductCategory.objects.create(name="test2", owner=self.user)
        
    def test_product_create_view(self):
        product = {
            'name': 'test',
            'price': 100,
            'currency': 'USD',
            'rank': 1,
            'product_category': self.product_category.id
        }
        request = self.factory.post(reverse('product_create'), data=product)
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=str(token.access_token))

       
        response = ProductCreateView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], product['name'])
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, product['name'])

    def test_product_create_view_with_invalid_data(self):
        product = {
            'name': 'test',
            'price': 'sdjna',
            'currency': '442',
            'rank': 1,
            'product_category': self.product_category.id
        }
        request = self.factory.post(reverse('product_create'), data=product)
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=str(token.access_token))

       
        response = ProductCreateView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_create_view_with_invalid_product_category(self):
        product = {
            'name': 'test',
            'price': 'sdjna',
            'currency': '442',
            'rank': 1,
            'product_category': 10
        }
        request = self.factory.post(reverse('product_create'), data=product)
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=str(token.access_token))

       
        response = ProductCreateView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_create_view_with_multiple_product(self):
        product =  [{
            'name': 'test',
            'price': 31,
            'currency': 'USD',
            'rank': 1,
            'product_category': self.product_category.id
        },
        {
            'name': 'test2',
            'price': 300,
            'currency': 'USD',
            'rank': 3,
            'product_category': self.product_category.id
        }]
        data = json.dumps(product)
        request = self.factory.post(reverse('product_create'), data=data, content_type='application/json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=str(token.access_token))

       
        response = ProductCreateView.as_view()(request)
       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[0]['name'], product[0]['name'])
        self.assertEqual(Product.objects.count(), 2)

class ProductUpdateViewTest(TestCase):

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
            product_category = self.product_category
        )
    def test_product_update_view(self):
        
        product = {
            'name': 'test updated',
            'price': 31,
            'currency': 'USD',
            'rank': 1,
            'product_category': self.product_category.id
        }
        request = self.factory.put(reverse('product_update', kwargs={'id': self.product.id}), data=product, content_type='application/json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=str(token.access_token))

        response = ProductUpdateView.as_view()(request, id=self.product.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().name, product['name'])

    def test_product_update_view_with_missing_items(self):
        product = {
            'price': 31,
            'currency': 'USD',
            'product_category': self.product_category.id
        }
        request = self.factory.put(reverse('product_update', kwargs={'id': self.product.id}), data=product, content_type='application/json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=str(token.access_token))

        response = ProductUpdateView.as_view()(request, id=self.product.id)
      
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ProductDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email="test@example.com", password="123456")
        self.user2 = User.objects.create(email="test2@example.com", password="123456")
        self.product_category = ProductCategory.objects.create(name="test", owner=self.user)
        self.product = Product.objects.create(
            name='Product',
            price=50.00,
            currency='EUR',
            rank=9,
            owner=self.user,
            product_category = self.product_category
        )
    def test_product_delete_view(self):
       
        request = self.factory.delete(reverse('product_delete', kwargs={'id': self.product.id}))
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=str(token.access_token))

        response = ProductDeleteView.as_view()(request, id=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_product_delete_view_from_another_user(self):
        
        request = self.factory.delete(reverse('product_delete', kwargs={'id': self.product.id}))
        token = RefreshToken.for_user(self.user2)
        force_authenticate(request, self.user2, token=str(token.access_token))

        response = ProductDeleteView.as_view()(request, id=self.product.id)
    
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProductListViewTest(TestCase):
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
        self.product2 = Product.objects.create(
            name='Product2',
            price=50.00,
            currency='EUR',
            rank=9,
            owner=self.user,
            product_category = self.product_category,
        )
        

    def test_product_list_view(self):
        request = self.factory.get(reverse('products'))
        response = ProductListView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class CategoryCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email="test@example.com", password="123456")
        self.product_category = ProductCategory.objects.create(name="test", owner=self.user)
    
    def test_category_create_view(self):
        request = self.factory.post(reverse('categories_create'), data={'name': 'test'}, format='json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=str(token.access_token))

        response = CategoryCreateView.as_view()(request)
        
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'test')

    def test_category_create_view_with_missing_name(self):
        request = self.factory.post(reverse('categories_create'), data={}, format='json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=str(token.access_token))

        response = CategoryCreateView.as_view()(request)
        
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

