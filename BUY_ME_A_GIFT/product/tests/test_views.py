"""
This module contains test cases for testing:
 - Product creation
 - Product update
 - Product deletion
 - product listing
 - Product Category creation
 - Product category deletion
 - Product category listing
 - Wishlist creation
 - Wishlist deletion
 - Wishlist product listing

It contains testing enpoints having the above listed functionalities
"""

from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import force_authenticate
from rest_framework import status
from product.models import Product, ProductCategory, WishList
from product.views import (
    ProductView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductListView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    WishCreateView,
    WishListView,
    WishListUnauthorizedView
)
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import json


class ProductViewTest(TestCase):
    """
    This test cases test if a product can be returned
    given a valid product identifier
    """
    def setUp(self)  -> None:
        """
        Set up the test case.

        1. Create a user object wich will be used to create a product and product category
        2. Create a product category to be used to create a product
        3. create a product to test if it can be used in the view properly
        4. Create a request factory instance to make requests to the view
        """
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
        

    def test_product_view(self)  -> None:
        """
        This function test if product can be shown given the valid product id

        Request data:
         - product_id: valid product id
        """
        request = self.factory.get(reverse('product', kwargs={'id': self.product.id}))
        response = ProductView.as_view()(request, id=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_product_view_notfound(self)  -> None:
        """
        This function verify that a product can't be returned given
        a non-existing product id or invalid product id.

        Request data:
        - product_id: invalid product id
        """
        request = self.factory.get(reverse('product', kwargs={'id': 1000}))
        response = ProductView.as_view()(request, id=1000)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ProductCreateViewTest(TestCase):
    """
    
    """
    def setUp(self)  -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create(email="test@example.com", password="123456")
        self.product_category = ProductCategory.objects.create(name="test", owner=self.user)
        self.product_category2 = ProductCategory.objects.create(name="test2", owner=self.user)
        
    def test_product_create_view(self)  -> None:
        product = {
            'name': 'test',
            'price': 100,
            'currency': 'USD',
            'rank': 1,
            'product_category': self.product_category.id
        }
        request = self.factory.post(reverse('product_create'), data=product)
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

       
        response = ProductCreateView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], product['name'])
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, product['name'])

    def test_product_create_view_with_invalid_data(self)  -> None:
        product = {
            'name': 'test',
            'price': 'sdjna',
            'currency': '442',
            'rank': 1,
            'product_category': self.product_category.id
        }
        request = self.factory.post(reverse('product_create'), data=product)
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

       
        response = ProductCreateView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_create_view_with_invalid_product_category(self)  -> None:
        product = { 
            'name': 'test',
            'price': 'sdjna',
            'currency': '442',
            'rank': 1,
            'product_category': 10
        }
        request = self.factory.post(reverse('product_create'), data=product)
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

       
        response = ProductCreateView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_create_view_with_multiple_product(self) -> None:
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
        force_authenticate(request, self.user, token=token.access_token)

       
        response = ProductCreateView.as_view()(request)
       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[0]['name'], product[0]['name'])
        self.assertEqual(Product.objects.count(), 2)

class ProductUpdateViewTest(TestCase):

    def setUp(self) -> None:
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
    def test_product_update_view(self) -> None:
        
        product = {
            'name': 'test updated',
            'price': 31,
            'currency': 'USD',
            'rank': 1,
            'product_category': self.product_category.id
        }
        request = self.factory.put(reverse('product_update', kwargs={'id': self.product.id}), data=product, content_type='application/json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = ProductUpdateView.as_view()(request, id=self.product.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().name, product['name'])

    def test_product_update_view_with_missing_items(self) -> None:
        product = {
            'price': 31,
            'currency': 'USD',
            'product_category': self.product_category.id
        }
        request = self.factory.put(reverse('product_update', kwargs={'id': self.product.id}), data=product, content_type='application/json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = ProductUpdateView.as_view()(request, id=self.product.id)
      
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ProductDeleteViewTest(TestCase):
    def setUp(self) -> None:
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
    def test_product_delete_view(self) -> None:
       
        request = self.factory.delete(reverse('product_delete', kwargs={'id': self.product.id}))
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = ProductDeleteView.as_view()(request, id=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_product_delete_view_from_another_user(self) -> None:
        
        request = self.factory.delete(reverse('product_delete', kwargs={'id': self.product.id}))
        token = RefreshToken.for_user(self.user2)
        force_authenticate(request, self.user2, token=token.access_token)

        response = ProductDeleteView.as_view()(request, id=self.product.id)
    
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProductListViewTest(TestCase):
    def setUp(self) -> None:
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
        

    def test_product_list_view(self) -> None:
        request = self.factory.get(reverse('products'))
        response = ProductListView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class CategoryCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create(email="test@example.com", password="123456")
        self.product_category = ProductCategory.objects.create(name="test", owner=self.user)
    
    def test_category_create_view(self) -> None:
        request = self.factory.post(reverse('categories_create'), data={'name': 'test'}, format='json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = CategoryCreateView.as_view()(request)
        
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'test')

    def test_category_create_view_with_missing_name(self) -> None:
        request = self.factory.post(reverse('categories_create'), data={}, format='json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = CategoryCreateView.as_view()(request)
        
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CategoryDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create(email="test@example.com", password="123456")
        self.user2 = User.objects.create(email="test2@example.com", password="123456")
        self.product_category = ProductCategory.objects.create(name="test", owner=self.user)

    def test_category_delete_view(self) -> None:
        request = self.factory.delete(reverse('category_delete', kwargs={'id': self.product_category.id}))
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = CategoryDeleteView.as_view()(request, id=self.product_category.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ProductCategory.objects.count(), 0)

    def test_category_delete_view_from_another_user(self) -> None:
        request = self.factory.delete(reverse('category_delete', kwargs={'id': self.product_category.id}))
        token = RefreshToken.for_user(self.user2)
        force_authenticate(request, self.user2, token=token.access_token)

        response = CategoryDeleteView.as_view()(request, id=self.product_category.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CategoryListViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create(email="test@example.com", password="123456")
        self.user2 = User.objects.create(email="test2@example.com", password="123456")
        self.product_category = ProductCategory.objects.create(name="test", owner=self.user)
        self.product_category2 = ProductCategory.objects.create(name="test1", owner=self.user)

    
    def test_category_list_view(self) -> None:
        request = self.factory.get(reverse('categories'))
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = CategoryListView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def category_list_view_from_another_user(self) -> None:

        request = self.factory.get(reverse('categories'))
        token = RefreshToken.for_user(self.user2)
        force_authenticate(request, self.user2, token=token.access_token)

        response = CategoryListView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class WishListCreateViewTest(TestCase):
    def setUp(self) -> None:
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
    
    def test_wishlist_create_view(self) -> None:
        data = {
            'product_id': self.product.id
        }
        request = self.factory.post(reverse('wishlist_create'), data=data, format='json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = WishCreateView.as_view()(request)
        
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product_id'], self.product.id)

    def test_wishlist_create_view_with_missing_product_id(self) -> None:
        request = self.factory.post(reverse('wishlist_create'), data={}, format='json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = CategoryCreateView.as_view()(request)
        
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_wishlist_create_view_add_multiple_product_from_same_category(self) -> None:
        data = {
            'product_id': self.product.id
        }
        request = self.factory.post(reverse('wishlist_create'), data=data, format='json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = WishCreateView.as_view()(request)
        
        data = {
            'product_id': self.product2.id
        }
        request = self.factory.post(reverse('wishlist_create'), data=data, format='json')
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = WishCreateView.as_view()(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class WishListViewTest(TestCase):
    def setUp(self) -> None:
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
            product_category = self.product_category,
        )
        self.wishlist = WishList.objects.create(user=self.user)
        self.wishlist.products.add(self.product)

    def test_wishlist_view(self) -> None:
        request = self.factory.get(reverse('wishlist'))
        token = RefreshToken.for_user(self.user)
        force_authenticate(request, self.user, token=token.access_token)

        response = WishListView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WishListUnauthTest(TestCase):
    def setUp(self) -> None:
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
            product_category = self.product_category,
        )
        self.wishlist = WishList.objects.create(user=self.user)
        self.wishlist.products.add(self.product)
    
    def test_wishlist_any_access_view(self) -> None:
        request = self.factory.get(reverse('wish_list_unauthorized', kwargs={'uuid': self.user.id}))
        

        response = WishListUnauthorizedView.as_view()(request, uuid=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_wishlist_any_access_view_with_invalid_uuid(self) -> None:
        request = self.factory.get(reverse('wish_list_unauthorized', kwargs={'uuid': 'aead'}))
        
        response = WishListUnauthorizedView.as_view()(request, uuid=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)