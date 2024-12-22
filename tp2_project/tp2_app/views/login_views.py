from django.shortcuts import render


def login(request):
    context = {
        'username': 'Guest',
    }
    return render(request, 'login.html', context)