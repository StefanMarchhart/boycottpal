from django.shortcuts import render


# Create your views here.

def landing(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'home.html')
