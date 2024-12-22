from django.http import HttpResponse

def home(request):
    return HttpResponse("<html><body><p>home</p></body></html>")