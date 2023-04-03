from django.test import TestCase
from product.models import ProductCategory, Product, WishList
from product.serializers import (
    ProductCategorySerializer,
    ProductCategoryCreateSerializer,
    ProductCreateSerializer,
    ProductListSerializer,
    WishListSerializer,
    WishListCreateSerializer,
    WishListUnauthorizedSerializer
)
from user.models import User
from unittest.mock import Mock

class ProductCategorySerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='example@example.com')
        self.category = ProductCategory.objects.create(name='Test Category', owner=self.user)

    def test_product_category_serializer(self) -> None:
        serializer = ProductCategorySerializer(self.category)
        expected_fields = set(['id', 'name', 'owner'])
        self.assertCountEqual(serializer.data.keys(), expected_fields)

class ProductCategoryCreateSerializerTestCase(TestCase):
    def test_product_category_create_serializer(self) -> None:
        data = {'name': 'New Category'}
        serializer = ProductCategoryCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertCountEqual(serializer.validated_data.keys(), ['name'])

class ProductCreateSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='example@example.com')
        self.category = ProductCategory.objects.create(name='Test Category', owner=self.user)
        self.category.save()
        self.product_data = {
            'name': 'Test Product',
            'price': 10.0,
            'rank': 1,
            'product_category': self.category.id
        }

    def test_product_create_serializer(self) -> None:
        serializer = ProductCreateSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        self.assertCountEqual(serializer.validated_data.keys(), ['name', 'price', 'rank', 'product_category'])

class ProductListSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='example@example.com')
        self.category = ProductCategory.objects.create(name='Test Category', owner=self.user)
        self.product = Product.objects.create(
            name='Test Product',
            price=10.0,
            rank=1,
            product_category=self.category,
            owner=self.user
        )

    def test_product_list_serializer(self) -> None:
        serializer = ProductListSerializer(self.product)
        expected_fields = set(['id', 'name', 'price', 'created_time', 'product_category'])
        self.assertCountEqual(serializer.data.keys(), expected_fields)

class WishListSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='example@example.com')
        self.category = ProductCategory.objects.create(name='Test Category', owner=self.user)
        self.product = Product.objects.create(
            name='Test Product',
            price=10.0,
            rank=1,
            product_category=self.category,
            owner=self.user
        )
        self.wishlist = WishList.objects.create(user=self.user)
        self.wishlist.products.add(self.product)

    def test_wishlist_serializer(self) -> None:
        serializer = WishListSerializer(self.wishlist)
        self.assertEqual(serializer.data['products'][0]['id'], self.product.id)

class WishListCreateSerializerTestCase(TestCase):
    def setUp(self)  -> None:
        self.user = User.objects.create_user(email='example@example.com')
        self.category = ProductCategory.objects.create(name='Test Category', owner=self.user)
        self.product = Product.objects.create(
            name='Test Product',
            price=10.0,
            rank=1,
            product_category=self.category,
            owner=self.user
        )
        self.user = User.objects.create(email='testuser@abcde.com')
        self.context = {'request': Mock(user=self.user)}

    def test_wishlist_create_serializer(self) -> None:
        data = {'product_id': self.product.id}
        serializer = WishListCreateSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        self.assertCountEqual(serializer.validated_data.keys(), ['product_id'])

class WishListUnauthorizedSerializerTestCase(TestCase):
    def setUp(self)  -> None:
        self.user = User.objects.create_user(email='example@example.com')
        self.category = ProductCategory.objects.create(name='Test Category', owner=self.user)
        self.product = Product.objects.create(
            name='Test Product',
            price=10.0,
            rank=1,
            product_category=self.category,
            owner=self.user
        )
        self.wishlist = WishList.objects.create(user=self.user)
        self.wishlist.products.add(self.product)

    def test_wishlist_unauthorized_serializer(self)  -> None:
        serializer = WishListUnauthorizedSerializer(self.wishlist)
        self.assertEqual(serializer.data['products'][0]['id'], self.product.id)