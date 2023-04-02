from django.urls import path
from .views import LoginView, SignUpView, PasswordResetView, PasswordResetTokenCheckView, SetNewPasswordApiView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('password_reset', PasswordResetView.as_view(), name='reset'),
    path('password_reset/<uidb64>/<token>', PasswordResetTokenCheckView.as_view(), name='password_reset'),
    path('password_reset_done', SetNewPasswordApiView.as_view(), name='password_reset_done'),
]
