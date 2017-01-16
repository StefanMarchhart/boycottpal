from account.forms import UserForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
import json
from uszipcode import ZipcodeSearchEngine
import operator


# Create your views here.
def home(request):
    # return HttpResponse('Hello from Python!')
    decoded_json=[]
    raw_alert = request.GET.get('alert')
    if raw_alert == None:
        alert=""
    else:
        alert=raw_alert
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
                'id': boycott.id,
                'target_id':boycott.target.id
            }
            boycotts.append(bct)
        decoded_json = json.loads(json.dumps(boycotts))


    # x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
    # sorted_x = sorted(x.items(), key=operator.itemgetter(1))



    return render(request, 'home.html',{'alert':alert, 'my_boycotts': decoded_json})



def Signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            # process data in form
            user = form.save()


            user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    )


            if user is not None:
                login(request, user)
            return HttpResponseRedirect('/?alert=signup')

        # new_user = authenticate(username=form.cleaned_data['username'],
        #                         password=form.cleaned_data['password1'],
        #                         )
        # login(request, new_user)

    else:
        form = UserForm()


    return render(request, 'signup.html', {'form': form})

