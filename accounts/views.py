from django.shortcuts import render
from core.logs.logger import logger

def user_login(request):
    context = {}
    return render(request, 'accounts/login.html', context)