from django.test import TestCase
from user.models import User
from product.models import ProductCategory, Product, WishList


class ProductCategoryModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='testuser@test.com')
        self.category = ProductCategory.objects.create(name='testcategory', owner=self.user)

    def test_product_category_creation(self) -> None:
        self.assertEqual(self.category.name, 'testcategory')
        self.assertEqual(self.category.owner, self.user)
    def test_product_category_deletion(self) -> None:
        self.category.delete()
        self.assertEqual(ProductCategory.objects.count(), 0)
    def test_product_category_deletion_upon_user_deletion(self) -> None:
        self.assertEqual(ProductCategory.objects.count(), 1)
        self.user.delete()
        self.assertEqual(ProductCategory.objects.count(), 0)


class ProductModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='testuser@test.com')
        self.category = ProductCategory.objects.create(name='testcategory', owner=self.user)
        self.product = Product.objects.create(name='testproduct', price=10.0, currency='USD', rank=1, product_category=self.category, owner=self.user)

    def test_product_creation(self) -> None:
        self.assertEqual(self.product.name, 'testproduct')
        self.assertEqual(self.product.price, 10.0)
        self.assertEqual(self.product.currency, 'USD')
        self.assertEqual(self.product.rank, 1)
        self.assertEqual(self.product.product_category, self.category)
        self.assertEqual(self.product.owner, self.user)

    def test_product_deletion(self) -> None:
        self.product.delete()
        self.assertEqual(Product.objects.count(), 0)
    
    def test_product_deletion_upon_user_deletion(self) -> None:
        self.assertEqual(Product.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Product.objects.count(), 0)
    def test_product_deletion_upon_category_deletion(self) -> None:
        self.assertEqual(Product.objects.count(), 1)
        self.category.delete()
        self.assertEqual(Product.objects.count(), 0)

class WishListModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='testuser@test.com')
        self.category = ProductCategory.objects.create(name='testcategory', owner=self.user)
        self.product = Product.objects.create(name='testproduct', price=10.0, currency='USD', rank=1, product_category=self.category, owner=self.user)
        self.wishlist = WishList.objects.create(user=self.user)

    def test_wishlist_add_product(self) -> None:
        self.wishlist.products.add(self.product)
        self.assertEqual(self.wishlist.products.count(), 1)
        self.assertEqual(self.wishlist.products.first(), self.product)

    def test_wishlist_deletion(self) -> None:
        self.wishlist.delete()
        self.assertEqual(WishList.objects.count(), 0)
    def test_wishlist_deletion_upon_user_deletion(self) -> None:
        self.assertEqual(WishList.objects.count(), 1)
        self.user.delete()
        self.assertEqual(WishList.objects.count(), 0)