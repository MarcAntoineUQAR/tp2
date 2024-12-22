from django.shortcuts import render, redirect
from django.urls import reverse
import requests
from rest_framework import status

def register(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        data = {
            "username": request.POST.get('username'),
            "firstname": request.POST.get('firstname'),
            "lastname": request.POST.get('lastname'),
            "email": request.POST.get('email'),
            "password": request.POST.get('password'),
        }

        if role == 'client':
            data["phone_number"] = request.POST.get('phone_number')
            data["address"] = request.POST.get('address')
            url = reverse('client-create')
        else:
            data["salary"] = request.POST.get('salary', 0)
            url = reverse('mechanic-create')

        response = requests.post(request.build_absolute_uri(url), json=data)
        
        if response.status_code == status.HTTP_201_CREATED:
            return redirect('login')
        else:
            context = {
                'error': response.json(),
                'form_data': request.POST
            }
            return render(request, 'register.html', context)
    
    return render(request, 'register.html')
