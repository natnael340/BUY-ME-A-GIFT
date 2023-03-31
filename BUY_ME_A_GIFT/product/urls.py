from django.urls import path
from .views import ProductListView, ProductCreateView, CategoryListView, CategoryCreateView

urlpatterns = [
    path('products', ProductListView.as_view(), name='products'),
    path('products/add', ProductCreateView.as_view(), name='product_create'),
    path('categories', CategoryListView.as_view(), name='categories'),
    path('categories/add', CategoryCreateView.as_view(), name='categories_create'),
]
