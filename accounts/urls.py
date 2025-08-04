from django.urls import path
from accounts import views as accounts_views

urlpatterns = [
    path('', accounts_views.user_login, name='login'),
]
