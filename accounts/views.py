from django.shortcuts import render

def user_login(request):
    context = {}
    return render(request, 'accounts/landing.html', context)