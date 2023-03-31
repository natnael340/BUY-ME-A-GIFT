from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Product, ProductCategory
from .serializers import ProductCreateSerializer, ProductListSerializer, ProductCategorySerializer, ProductCategoryCreateSerializer
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
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

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