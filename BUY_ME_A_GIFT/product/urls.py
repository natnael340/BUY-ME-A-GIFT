from django.urls import path
from .views import ProductListView, ProductCreateView, CategoryListView, CategoryCreateView, ProductUpdateView, CategoryUpdateView

urlpatterns = [
    path('products', ProductListView.as_view(), name='products'),
    path('products/add', ProductCreateView.as_view(), name='product_create'),
    path('products/edit/<int:id>', ProductUpdateView.as_view(), name='product_update'),
    path('categories', CategoryListView.as_view(), name='categories'),
    path('categories/add', CategoryCreateView.as_view(), name='categories_create'),
    path('categories/edit/<int:id>', CategoryUpdateView.as_view(), name='category_update'),

]
