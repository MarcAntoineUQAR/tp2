from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from tp2_app.models import Client, Mechanic
from django.contrib.auth import authenticate

def login(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        client = Client.objects.filter(username=username).first()
        mechanic = Mechanic.objects.filter(username=username).first()
        
        if client and check_password(password, client.password):
            message = f"Welcome, {client.username}!"
        elif mechanic and check_password(password, mechanic.password):
            message = f"Welcome, {mechanic.username}!"
        else:
            message = "Invalid username or password."

    return render(request, 'login.html', {'message': message})
