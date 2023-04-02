from django.urls import path
from .views import LoginView, SignUpView, PasswordResetView, PasswordResetTokenCheckView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('password_reset', PasswordResetView.as_view(), name='reset'),
    path('password_reset/token', PasswordResetTokenCheckView.as_view(), name='password_reset'),
]
