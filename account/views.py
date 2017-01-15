from account.forms import UserForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            # process data in form
            user = form.save()

            logging_in = authenticate(username=user.username, password=user.password)
            if logging_in is not None:
                login(request, logging_in)
            return HttpResponseRedirect('/')

    else:
        form = UserForm()


    return render(request, 'signup.html', {'form': form})

