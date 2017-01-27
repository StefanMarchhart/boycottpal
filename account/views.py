from account.forms import UserForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
import json
from uszipcode import ZipcodeSearchEngine
import operator
from boycotted.models import *
import datetime


# Create your views here.
def home(request):
    my_boycotts_json=[]
    top_boycotts_json=[]
    trending_boycotts_json=[]
    raw_alert = request.GET.get('alert')
    if raw_alert == None:
        alert=""
    else:
        alert=raw_alert
    if request.user.is_authenticated():
        my_boycotts=[]
        for my_boycott in request.user.boycotts.all():
            zip=my_boycott.target.zip
            if zip == "":
                location = " "
            else:
                search = ZipcodeSearchEngine()
                location = search.by_zipcode(zip)

                location = "("+ str(location.City) + ", " + str(location.State)+") "

            my_bct = {
                'name':my_boycott.target.name,
                'location':location,
                'reason':my_boycott.reason,
                'id': my_boycott.id,
                'target_id':my_boycott.target.id
            }
            my_boycotts.append(my_bct)

        my_boycotts_json = json.loads(json.dumps(my_boycotts))
    trending_boycotts=[]
    top_boycotts=[]
    for top_boycott in Boycotted.objects.all():
        zip = top_boycott.zip
        if zip == "":
            location = " "
        else:
            search = ZipcodeSearchEngine()
            location = search.by_zipcode(zip)

            location = "(" + str(location.City) + ", " + str(location.State) + ") "



        top_bct={
            'name':top_boycott.name,
            'id':top_boycott.id,
            'num':top_boycott.boycotts.count(),
            'location':location
        }
        top_boycotts.append(top_bct)

    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)

    for trending_boycott in Boycotted.objects.filter(date__range=[start_week,end_week]):
        zip = trending_boycott.zip
        if zip == "":
            location = " "
        else:
            search = ZipcodeSearchEngine()
            location = search.by_zipcode(zip)

            location = "(" + str(location.City) + ", " + str(location.State) + ") "

        trend_bct={
            'name':trending_boycott.name,
            'id':trending_boycott.id,
            'num':trending_boycott.boycotts.count(),
            'location':location
        }
        trending_boycotts.append(trend_bct)

    def getKey(boycott):
        return int(boycott['num'])

    top_boycotts_json = json.loads(json.dumps(sorted(top_boycotts, key=getKey, reverse=True)[:25]))
    trending_boycotts_json = json.loads(json.dumps(sorted(trending_boycotts, key=getKey, reverse=True)[:10]))







    return render(request, 'home.html',{
        'alert':alert,
        'my_boycotts': my_boycotts_json,
        'top_boycotts':top_boycotts_json,
        'trending_boycotts':trending_boycotts_json
    })



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

