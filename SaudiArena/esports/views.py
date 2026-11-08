
from django.shortcuts import render


def home(request):
    return render(request, 'esports/home.html')