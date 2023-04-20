from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from .models import Product, ProductCategory, WishList
from .serializers import ProductCreateSerializer, ProductListSerializer, ProductCategorySerializer, ProductCategoryCreateSerializer, WishListSerializer, WishListCreateSerializer, WishListUnauthorizedSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from uuid import uuid4
from user.models import User
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from typing import Any
from django.db.models.query import QuerySet

# Create your views here.

class ISAuthorized(BasePermission):
    def has_object_permission(self, request: Request, view: Any, obj: Product|ProductCategory) -> bool:
        if obj.owner == request.user:
            return True
        return False
@swagger_auto_schema(security=[])    
class ProductView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    @swagger_auto_schema(security=[])
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: Any) -> None:
        serializer.save(owner=self.request.user)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=self.request.data, many=isinstance(self.request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductUpdateView(UpdateAPIView):
    
    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductCreateSerializer
    permission_classes=[IsAuthenticated & ISAuthorized]
    lookup_field = 'id'
class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    def get_queryset(self) -> QuerySet[Product]:
        queryset = Product.objects.all()
        price_gt = self.request.query_params.get('price_gt', None)
        price_lt = self.request.query_params.get('price_lt', None)

        if price_gt:
            queryset = queryset.filter(price__gt=price_gt)
        if price_lt:
            queryset = queryset.filter(price__lt=price_lt)
        
        return queryset
    
    @swagger_auto_schema(security=[])
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
    
class ProductDeleteView(DestroyAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, ISAuthorized]
    lookup_field='id'

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryListView(ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated, ISAuthorized]


class CategoryCreateView(CreateAPIView):
    queryset = ProductCategory.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductCategoryCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: Any) -> None:
        serializer.save(owner=self.request.user)
class CategoryDeleteView(DestroyAPIView):
    queryset = ProductCategory.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductCategorySerializer
    permission_classes=[IsAuthenticated & ISAuthorized]
    lookup_field = 'id'

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
class WishListView(RetrieveAPIView):
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> WishList:
        user = self.request.user
        wishlist, _ = WishList.objects.prefetch_related('products').get_or_create(user=user)
        return wishlist

class WishCreateView(CreateAPIView):
    serializer_class = WishListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self) -> dict:
        return {'request': self.request}

class WishListUnauthorizedView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self) -> QuerySet[Product]:
        try:
            user = User.objects.get(id=self.kwargs['uuid'])
        except User.DoesNotExist:
            user = None
        
        created_time = self.request.query_params.get('created_time', None)
        rank = self.request.query_params.get('rank', None)

        queryset = Product.objects.filter(whishlist_products__user = user)

        if created_time:
            if created_time == 'asc':
                queryset = queryset.order_by('-created_time')
            else:
                queryset = queryset.order_by('created_time')
        if rank:
            if rank == 'asc':
                queryset = queryset.order_by('-rank')
            else:
                queryset = queryset.order_by('rank')

        return queryset
    
    @swagger_auto_schema(security=[])
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)