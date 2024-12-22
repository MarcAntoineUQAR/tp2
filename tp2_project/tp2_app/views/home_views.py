from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("<html><body><p>home</p></body></html>")

def lobby(request):
    return render(request, 'lobby.html')