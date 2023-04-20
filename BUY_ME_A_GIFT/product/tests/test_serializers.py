"""
This module contains test cases for serializers in the product application.

It includes the following serializers:
- ProductCategorySerializer
- ProductCategoryCreateSerializer
- ProductCreateSerializer
- ProductListSerializer
- WishListSerializer
- WishListCreateSerializer
- WishListUnauthorizedSerializer

"""

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
    """
    Test for ProductCategorySerializer checking if 
    the product object data and the serilized data match
    """
    def setUp(self) -> None:
        """
        Set Up test cases

        Create user and create product category using the user object
        """
        self.user = User.objects.create_user(email='example@example.com')
        self.category = ProductCategory.objects.create(name='Test Category', owner=self.user)

    def test_product_category_serializer(self) -> None:
        """
        Test ProductCategorySerializer if the product category created data matches the serialized data
        
        Arguments:
         - product category
        
        Raises assert error if the serialized key does not match the category keys which are:
         - id
         - name
         - owner
        """
        serializer = ProductCategorySerializer(self.category)
        expected_fields = set(['id', 'name', 'owner'])
        self.assertCountEqual(serializer.data.keys(), expected_fields)

class ProductCategoryCreateSerializerTestCase(TestCase):
    """
    Test ProductCategoryCreateSerializer to check serialization
    of user input to create a product category works correctly

    """
    def test_product_category_create_serializer(self) -> None:
        """
        Test ProductCategoryCreateSerializer to createt a product

        Arguments:
         - name

        Raises assert error if the serializer is not valid given the correct arguments or
        if the validated data keys is different from `name`.

        """
        data = {'name': 'New Category'}
        serializer = ProductCategoryCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertCountEqual(serializer.validated_data.keys(), ['name'])

class ProductCreateSerializerTestCase(TestCase):
    """
    This test checks if ProductCreateSerializer serializes the user supplied data correctly
    """
    def setUp(self) -> None:
        """
        Setup test case

        create user and category objects which are used to create product given the owner and category
        """
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
        """
        This test method create product given the valid product arguments

        Arguments:
         - name: The name of the product
         - price: The price of the product
         - rank: The rank of the product
         - product_category: The category of the product

        Expected result: Since the provided arguments are valid the serializer should be valid and 
        the returned key should match the provided arguments
        """
        serializer = ProductCreateSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        self.assertCountEqual(serializer.validated_data.keys(), ['name', 'price', 'rank', 'product_category'])

class ProductListSerializerTestCase(TestCase):
    """
    This test verifies that the ProductListSerializer list the list of products
    """
    def setUp(self) -> None:
        """
        Set up the test case.

        Creaet a user, category, and product for testing listing serialization
        """
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
        """
        This test case verifies that all the product added in the setup phases
        are returned after serialization

        Expected result: all the product added in the setup phases. and the test 
        checks if the keys returned mathced the following keys
        - id
        - name
        - price
        - created_time
        - product_category

        Raises assertion error if the expected result is not found
        """
        serializer = ProductListSerializer(self.product)
        expected_fields = set(['id', 'name', 'price', 'created_time', 'product_category'])
        self.assertCountEqual(serializer.data.keys(), expected_fields)

class WishListSerializerTestCase(TestCase):
    """
    This test verifies that the WishListSerializer list the all the wish lists in the database
    """
    def setUp(self) -> None:
        """
        Set up test case

        Create user, product category and product. 
        Then add this product to the wish list in coresponding 
        users wish list
        """
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
        """
        This test the WishListSerializer list all the products 
        given the wishlist object

        Arguments:
         - wishlist: wishlist object

        Expected result: all products(id) added to wishlist. 

        Raises assertion error if the product in the wishlist object 
        is not in the serialized wishlist object
        """
        serializer = WishListSerializer(self.wishlist)
        self.assertEqual(serializer.data['products'][0]['id'], self.product.id)

class WishListCreateSerializerTestCase(TestCase):
    """
    This test verifies that the WishListCreateSerializer create wishlist object 
    for a user and add products to the user wishlist
    """
    def setUp(self)  -> None:
        """
        Setup test cases

        Create user, catgory and category which are used to create wishlist 
        for a custom user
        """
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
        """
        This test if a random user which is not the owner of the product
        can create a wish and add products to the wish list

        Arguments:
         - product_id: The product id to be added to the wish list
         - user: The user who is adding products to the wish list

        Expected result: For the wish list to be vaid given a valid input and 
        the serializer should return the product id added to the wish list

        Raise assertion error if the expected result is not met
        """
        data = {'product_id': self.product.id}
        serializer = WishListCreateSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        self.assertCountEqual(serializer.validated_data.keys(), ['product_id'])

class WishListUnauthorizedSerializerTestCase(TestCase):
    """
    This test case tests if an authorized user can access
    wishlist of other users
    """
    def setUp(self)  -> None:
        """
        Set up the test cases

        Create user, product category, product and wishlist fot the user.
        """
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
        """
        Test if wishlist of some user can be accessed for unauthorized user

        Arguments:
         - wishlist: wishlist of some user

        Expected result: list of Products which belongs to wishlist object

        Raises assertion error if added product doesn't match with the serialized
        product
        """
        serializer = WishListUnauthorizedSerializer(self.wishlist)
        self.assertEqual(serializer.data['products'][0]['id'], self.product.id)