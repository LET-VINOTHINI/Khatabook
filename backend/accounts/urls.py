from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, MeView, VerifyPinView, BackupNowView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('verify-pin/', VerifyPinView.as_view(), name='verify-pin'),
    path('backup/', BackupNowView.as_view(), name='backup'),
]
