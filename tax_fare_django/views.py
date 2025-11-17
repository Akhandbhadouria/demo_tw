# from django.shortcuts import render

# def home_page(request):
#     return render(request,"index.html")
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

def home(request):
    total_users = User.objects.count()
    return render(request, "home.html", {"total_users": total_users})
