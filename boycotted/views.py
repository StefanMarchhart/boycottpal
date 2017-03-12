from datetime import datetime
import requests
from account.views import _get_disqus_sso
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from boycott.general import process_zip
from boycott.settings import SERVER
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
        boycotted=[]
        if boycotted_form.is_valid() and boycott_form.is_valid():
            # Save boycotted values to access
            temp_boycotted = boycotted_form.save(commit=False)

            # Check to see if boycotted exists already
            boycotted_query = Boycotted.objects.filter(name=temp_boycotted.name).filter(zip=temp_boycotted.zip)
            if boycotted_query.count() > 0:
            #     If the boycotted exists already, fetch it.
                boycotted = boycotted_query[0]
            else:
                # boycotted = boycotted_form.save(commit=False)
                boycotted = boycotted_form.save()
                # boycotted.date = datetime.now()
                # boycotted.save()

            # process data in form
            boycott = boycott_form.save(commit=False)
            boycott.boycotter = request.user
            # boycott.date = datetime.now()
            boycott.target = boycotted
            boycott.save()

            boycotted.boycotts.add(boycott)
            boycotted.save()
            request.user.boycotts.add(boycott)
            return HttpResponseRedirect('/boycotted/view/'+str(boycotted.id))

    else:
        boycott_form = BoycottForm()
        boycotted_form = BoycottedForm()
        boycotted=[]
        for boycott in Boycotted.objects.all():
            boycotted.append(boycott.name)




    return render(request, 'add_boycott.html', {
        'boycott_form': boycott_form,
        'boycotted_form':boycotted_form,
        'boycotted':json.loads(json.dumps(boycotted))
    })


# @login_required(login_url='/login/')
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
            'reason':boycott.reason,
            'id':boycott.id
        }
        boycotts.append(boy)
    decoded_json = json.loads(json.dumps(boycotts))


    disqus_sso = _get_disqus_sso(request.user)

    identifier= SERVER+'-Boycotted-'+boycotted_id


    IncrementComment(request, identifier)

    return render(request, 'view_boycotted.html', {
        'name': boycotted.name,
        'zip': zip,
        'location': location,
        'boycotts': decoded_json,
        "disqus_sso": disqus_sso,
        'id':boycotted_id
    })


@login_required(login_url='/login/')
def EditBoycott(request,boycott_id):
    prnt=''
    boycott = Boycott.objects.get(id=boycott_id)
    if request.user.username != boycott.boycotter.username:
        return HttpResponseRedirect('/')

    if boycott.target.zip == "":
        zip=""
        location = ""
    else:
        zip=boycott.target.zip
        search = ZipcodeSearchEngine()
        location = search.by_zipcode(zip)
        location = "(" + str(location.City) + ", " + str(location.State) + ")"

    if request.method == 'POST':

        boycott_form = BoycottForm(data=request.POST, instance=boycott)
        tag_form = AdminTagForm(data=request.POST)
        if boycott_form.is_valid() and tag_form.is_valid():

            tag = str(int(tag_form.cleaned_data['tag']))

            target=Boycott.objects.get(id=boycott_id).target

            new_boycott = boycott_form.save(commit=False)

            boycott.reason=new_boycott.reason
            target.tag = int(tag)
            boycott.save()
            target.save()

            return HttpResponseRedirect('/')

    else:
        boycott_form = BoycottForm(instance=boycott)
        tag_form = AdminTagForm(instance=boycott)

    return render(request, 'edit_boycott.html',
                  {'boycott_form': boycott_form,
                   'tag_form':tag_form,
                   'name': boycott.target.name,
                   'location': location,
                   'boycott_id': boycott_id,
                   'prnt':prnt
                   })


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def EditBoycotted(request,boycotted_id):

    boycotted = Boycotted.objects.get(id=boycotted_id)

    if boycotted.zip == "":
        zip=""
        location = ""
    else:
        zip=boycotted.zip
        search = ZipcodeSearchEngine()
        location = search.by_zipcode(zip)
        location = "(" + str(location.City) + ", " + str(location.State) + ")"


    if request.method == 'POST':
        print('actuallyposting')
        boycotted_form = BoycottedForm(data=request.POST)

        tag =  boycotted_form.data['tag']
        # new_boycotted = boycotted_form.save(commit=False)

        boycotted.tag = tag
        boycotted.save()
        return HttpResponseRedirect('/boycotted/view/all/')

    else:
        boycotted_form = BoycottedForm(instance=boycotted)

    return render(request, 'edit_boycotted.html',
                  {'boycotted_form': boycotted_form,
                   'name': boycotted.name,
                   'location': location,
                   'boycotted_id': boycotted_id,

                   })


@login_required(login_url='/login/')
def DeleteBoycott(request, boycott_id):
    boycott = Boycott.objects.get(id=boycott_id)
    if not request.user.is_superuser:
        if request.user.username != boycott.boycotter.username:
            return HttpResponseRedirect('/boycotted/view/all/')
    boycotted=boycott.target
    boycott.delete()
    if boycotted.boycotts.count()==0:
        boycotted.delete()


    return HttpResponseRedirect('/')

def ViewAllBoycotted(request):
        all_boycotted = []
        for bct in Boycotted.objects.all():

            pol = {
                'name': bct.name,
                'id': bct.id,
                "location": process_zip(bct.zip)
            }
            all_boycotted.append(pol)

        return render(request, 'view_all_boycotted.html', {
            'all_boycotted': all_boycotted
        })

@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def DeleteBoycotted(request, boycotted_id):
    boycotted = Boycotted.objects.get(id=boycotted_id)

    boycotted.delete()


    return HttpResponseRedirect('/')

def IncrementComment(request,identifier):

    params=identifier.split('-')
    boycotted= Boycotted.objects.get(id=params[2])

    params={
        "api_key":"UCkYzgSPnP4OtgopaqnhrhMrQnL6a8hJBvfzslmbB80N1jCaTexRI7mmVBumkoBO",
        "forum":'boycottpal',
        'thread:ident':identifier
    }
    r= requests.get('https://disqus.com/api/3.0/threads/details.json',params=params)
    comments=int(r.json()['response']['posts'])
    boycotted.comment_count=comments

    boycotted.save()
    return HttpResponse('Increment successful. Count is now: '+str(comments))
