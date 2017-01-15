from datetime import datetime

from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from boycotted.forms import *
from boycotted.models import *
from uszipcode import ZipcodeSearchEngine
# Create your views here.
@login_required(login_url='/login/')
def AddBoycott(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        boycott_form = BoycottForm(data=request.POST)
        boycotted_form = BoycottedForm(data=request.POST)
        if boycotted_form.is_valid() and boycott_form.is_valid():
            # Save boycotted values to access
            temp_boycotted = boycotted_form.save(commit=False)
            print(temp_boycotted.name)
            print(temp_boycotted.zip)

            # Check to see if boycotted exists already
            boycotted_query = Boycotted.objects.filter(name=temp_boycotted.name).filter(zip=temp_boycotted.zip)
            if boycotted_query.count() > 0:
            #     If the boycotted exists already, fetch it.
                boycotted = boycotted_query[0]
            else:
                boycotted = boycotted_form.save()

            # process data in form
            boycott = boycott_form.save(commit=False)
            boycott.boycotter = request.user
            boycott.date = datetime.now()
            boycott.target = boycotted
            boycott.save()

            boycotted.boycotts.add(boycott)
            boycotted.save()
            request.user.boycotts.add(boycott)
            return HttpResponseRedirect('/')

    else:
        boycott_form = BoycottForm()
        boycotted_form = BoycottedForm()

    return render(request, 'add_boycott.html', {'boycott_form': boycott_form, 'boycotted_form':boycotted_form})


@login_required(login_url='/login/')
def ViewBoycotted(request,boycotted_id):
    # if this is a POST request we need to process the form data
    boycotts=[]
    boycotted=Boycotted.objects.get(id=boycotted_id)
    if boycotted.zip == "":
        zip=""
        location = ""
    else:
        zip=boycotted.zip
        search = ZipcodeSearchEngine()
        location = search.by_zipcode(zip)
        location = "(" + str(location.City) + ", " + str(location.State) + ")"
    for boycott in boycotted.boycotts.all():
        boy={
            'username':boycott.boycotter.username,
            'date':boycott.date.strftime("%m/%d/%y"),
            'reason':boycott.reason
        }
        boycotts.append(boy)
    decoded_json = json.loads(json.dumps(boycotts))





    return render(request, 'view_boycotted.html', {
        'name': boycotted.name,
        'zip': zip,
        'location': location,
        'boycotts': decoded_json
    })
