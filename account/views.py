from account.forms import UserForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
import json
from uszipcode import ZipcodeSearchEngine


# Create your views here.
def home(request):
    # return HttpResponse('Hello from Python!')
    decoded_json=[]
    if request.user.is_authenticated():
        boycotts=[]
        for boycott in request.user.boycotts.all():
            zip=boycott.target.zip
            if zip == "":
                location = " "
            else:
                search = ZipcodeSearchEngine()
                location = search.by_zipcode(zip)

                location = "("+ str(location.City) + ", " + str(location.State)+") "

            bct = {
                'name':boycott.target.name,
                'location':location,
                'reason':boycott.reason,
                'id':boycott.target.id
            }
            boycotts.append(bct)
        decoded_json = json.loads(json.dumps(boycotts))



    return render(request, 'home.html',{'my_boycotts': decoded_json})



def Signup(request):
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

