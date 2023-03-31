from django.urls import path
from .views import LoginView, SignUpView, PasswordResetView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('password_reset', PasswordResetView.as_view(), name='reset'),
]
