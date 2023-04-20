"""BUY_ME_A_GIFT URL Configuration

The urlpattern contains routes for the whole application. These are
    1, route to the admin(default admin page)
    2, route to the product app(API)
    3, route to user app(API)
    4, route to refresh and verify token(API)

"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, TokenVerifyView )
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...
'''
The following options are set for generating
Swagger UI using the openapi library

'''
schema_view = get_schema_view(
   openapi.Info(
      title="BUY_ME_A_GIFT API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@vinhood.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/', include("product.urls")),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('api/user/', include("user.urls")),
]
