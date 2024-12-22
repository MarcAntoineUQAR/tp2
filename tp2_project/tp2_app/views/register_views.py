from django.shortcuts import render, redirect
from django.urls import reverse
import requests
from rest_framework import status


def register(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        data = {
            "username": request.POST.get('username'),
            "first_name": request.POST.get('first_name'),
            "last_name": request.POST.get('last_name'),
            "email": request.POST.get('email'),
            "password": request.POST.get('password'),
        }

        if role == 'client':
            data["phone_number"] = request.POST.get('phone_number')
            data["address"] = request.POST.get('address')
            url = request.build_absolute_uri(reverse('client-create'))
        else:
            data["salary"] = request.POST.get('salary', 0)
            url = request.build_absolute_uri(reverse('mechanic-create'))

        try:
            response = requests.post(url, json=data)
            if response.status_code == status.HTTP_201_CREATED:
                return redirect('login')
            else:
                context = {
                    'error': response.json() if response.headers.get(
                        'Content-Type') == 'application/json' else 'Unknown error',
                    'form_data': request.POST
                }
                return render(request, 'register.html', context)
        except requests.RequestException as e:
            context = {
                'error': str(e),
                'form_data': request.POST
            }
            return render(request, 'register.html', context)

    return render(request, 'register.html')
