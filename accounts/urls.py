from django.urls import path
from accounts import views as accounts_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', accounts_views.user_login, name='login'),
]
