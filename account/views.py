from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout

# Create your views here.
def home(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')