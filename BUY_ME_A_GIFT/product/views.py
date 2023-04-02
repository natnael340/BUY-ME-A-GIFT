from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Product, ProductCategory, WishList
from .serializers import ProductCreateSerializer, ProductListSerializer, ProductCategorySerializer, ProductCategoryCreateSerializer, WishListSerializer, WishListCreateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class ISAuthorized(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductUpdateView(UpdateAPIView):
    
    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductCreateSerializer
    permission_classes=[IsAuthenticated & ISAuthorized]
    lookup_field = id

class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        price_gt = self.request.query_params.get('price_gt', None)
        price_lt = self.request.query_params.get('price_lt', None)

        if price_gt:
            queryset = queryset.filter(price__gt=price_gt)
        if price_lt:
            queryset = queryset.filter(price__lt=price_lt)
        
        return queryset

class CategoryListView(ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class CategoryCreateView(CreateAPIView):
    queryset = ProductCategory.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductCategoryCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
class CategoryUpdateView(UpdateAPIView):
    queryset = ProductCategory.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductCategorySerializer
    permission_classes=[IsAuthenticated & ISAuthorized]
    lookup_field = 'id'

class WishListView(RetrieveAPIView):
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        wishlist, _ = WishList.objects.prefetch_related('products').get_or_create(user=user)
        return wishlist

class WishCreateView(CreateAPIView):
    serializer_class = WishListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}