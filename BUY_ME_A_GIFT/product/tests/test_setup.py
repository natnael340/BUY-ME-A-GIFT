from rest_framework.test import APITestCase
from django.urls import reverse
from product.views import (
    ProductView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductListView,
    CategoryCreateView,
    CategoryListView,
    CategoryDeleteView,
    WishCreateView,
    WishListView,
    WishListUnauthorizedView
)
from user.models import User

class TestSetup(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='test@example.com', password='testpassword')

        self.products_url = reverse('products')
        self.product_add_url = reverse('product_create')
        self.product_update_url = reverse('product_update')
        self.product_delete_url = reverse('product_delete')
        self.product_url = reverse('product', kwargs={'pk': 1})
        self.categories_url = reverse('categories')
        self.categories_add_url = reverse('category_create')
        self.categories_delete_url = reverse('category_delete', kwargs={'pk': 1})
        self.wishlist_url = reverse('wishlist')
        self.wishlist_add_url = reverse('wishlist_create')
        self.wishlist_anauth_url = reverse('wish_list_unauthorized', kwargs={"uid": '1'})

        return super().setUp()
    def tearDown(self):
        return super().tearDown()
