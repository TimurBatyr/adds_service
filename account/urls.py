from django.urls import path

from .views import RegistrationAPIView, ActivateView, LogoutView, ForgotPasswordView, ChangePasswordView, LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name="registration"),

    # path('login/', TokenObtainPairView.as_view(), name='login'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('activate/', ActivateView.as_view(), name="activation"),
    path('login/', LoginView.as_view(), name="signin"),
    path('logout/', LogoutView.as_view(), name="signout"),
    path('forgot_pass/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('change_password/', ChangePasswordView.as_view(), name="change-password"),
]