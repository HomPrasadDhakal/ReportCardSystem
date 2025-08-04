from django.shortcuts import render
from core.logs.logger import logger

def user_login(request):
    context = {}
    logger.info("User login view accessed")
    return render(request, 'accounts/login.html', context)