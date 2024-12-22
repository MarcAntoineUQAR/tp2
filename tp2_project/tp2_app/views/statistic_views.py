from django.shortcuts import render

def statistics(request):
    context = {
        'username': 'xX_Gooner69_Xx'
    }
    return render(request, 'statistic.html', context)