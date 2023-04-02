from django.urls import path
from .views import ProductListView, ProductCreateView, CategoryListView, CategoryCreateView, ProductUpdateView, CategoryDeleteView,WishListView, WishCreateView, WishListUnauthorizedView, ProductDeleteView, ProductView

urlpatterns = [
    path('products', ProductListView.as_view(), name='products'),
    path('products/add', ProductCreateView.as_view(), name='product_create'),
    path('products/edit/<int:id>', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:id>', ProductDeleteView.as_view, name='product_delete'),
    path('products/<int:id>', ProductView.as_view(), name='product'),
    path('categories', CategoryListView.as_view(), name='categories'),
    path('categories/add', CategoryCreateView.as_view(), name='categories_create'),
    path('categories/delete/<int:id>', CategoryDeleteView.as_view(), name='category_update'),
    path('wishlist', WishListView.as_view(), name='wishlist'),
    path('wishlist/add', WishCreateView.as_view(), name='wishlist_create'),
    path('wishlist/<uuid>', WishListUnauthorizedView.as_view(), name='wish_list_unauthorized'),

]
