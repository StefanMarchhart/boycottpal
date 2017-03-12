import os
import string
import random
import json
from django.conf import settings # import the settings file

from django.contrib.auth.decorators import login_required, user_passes_test

from account.disqus import get_disqus_sso
from account.forms import UserForm, ResetPasswordForm, TokenForm, ChangePasswordForm, ChangeEmailForm, EmailForm
from account.models import Token, BoycottUser
from account.models import HC
from boycott.general import process_zip
from boycotted.forms import FilterForm
from boycotted.models import *
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from uszipcode import ZipcodeSearchEngine
import operator
import datetime
import feedparser
from django.core.mail import send_mail
from boycott import settings as bct_settings
import feedparser

from polls.forms import NewPollForm
from polls.models import Poll

TOKEN_EXPIRE = datetime.timedelta(1)


def token_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Create your views here.
def home(request):
    # Hit counter
    if HC.objects.all().count()==0:
        HC.objects.create()
    else:
        hc= HC.objects.all()[0]
        hc.hits = hc.hits +1
        hc.save()

    # fetch and store RSS FEEDS
    cnn = feedparser.parse('http://rss.cnn.com/rss/cnn_topstories.rss')
    fox = feedparser.parse('http://feeds.foxnews.com/foxnews/latest')
    news = json.loads(json.dumps(list(zip(cnn.entries[:25], fox.entries[:25]))))

    my_boycotts_json = []
    # Handle Alerts
    raw_alert = request.GET.get('alert')
    if raw_alert == None:
        alert = ""
    else:
        alert = raw_alert

    if request.user.is_authenticated():
        my_boycotts = []
        for my_boycott in request.user.boycotts.all():
            zipcode = my_boycott.target.zip
            location = process_zip(zipcode)

            my_bct = {
                'name': my_boycott.target.name,
                'location': location,
                'reason': my_boycott.reason,
                'id': my_boycott.id,
                'target_id': my_boycott.target.id
            }
            my_boycotts.append(my_bct)

        my_boycotts_json = json.loads(json.dumps(my_boycotts))
    trending_boycotts = []
    # top_boycotts = []
    #




    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    lastMonth = datetime.date.today() + datetime.timedelta(days=-30)
    for trending_boycott in Boycotted.objects.filter(date__range=[lastMonth,tomorrow]):
        zipcode = trending_boycott.zip
        location = process_zip(zipcode)

        trend_bct = {
            'name': trending_boycott.name,
            'id': trending_boycott.id,
            'num': trending_boycott.boycotts.count(),
            'location': location
        }
        trending_boycotts.append(trend_bct)

    def sort_by_most(boycott):
        return int(boycott['num'])

    def sort_by_alpha(boycott):
        return str(boycott['name'])

    def sort_by_date(boycott):
        return str(datetime.datetime.strptime(boycott['date'], '%Y-%m-%d'))

    def sort_by_comments(boycott):
        return int(boycott['comment_count'])

    # top_boycotts_json = json.loads(json.dumps(sorted(top_boycotts, key=sort_by_most, reverse=True)[:25]))
    trending_boycotts_json = json.loads(json.dumps(sorted(trending_boycotts, key=sort_by_most, reverse=True)[:10]))

    prnt=''

    if request.method == 'POST':
        form = FilterForm(data=request.POST)
        if form.is_valid():
            # process data in form
            filter = form.save(commit=False)
            tag = str(int(form.cleaned_data['tag'])-1)
            sort = str(int(form.cleaned_data['sort'])-1)
            prnt="Tag Value-"+str(tag)+'| '+"Sort Value-"+str(sort)+'\n'



            tagged = Boycotted.objects.all()
            if int(tag) !=0:
                # prnt+=str(tagged.all())
                tagged=tagged.filter(tag=tag)
                print("filter")
                # prnt+="|"+str(tagged.all())

            if int(sort) ==2:
                # prnt+=str(tagged.all())
                tagged=tagged.order_by('-date')
                print("sorting by date")
                # prnt += "|" + str(tagged.all())




            all_boycotts=[]
            for boycott in tagged:
                zipcode = boycott.zip
                location = process_zip(zipcode)

                top_bct = {
                    'name': boycott.name,
                    'id': boycott.id,
                    'num': boycott.boycotts.count(),
                    'location': location,
                    'comment_count': boycott.comment_count
                }
                all_boycotts.append(top_bct)


            if sort == str(0):
                all_boycotts=sorted(all_boycotts, key=sort_by_most, reverse=True)
                print("sorting by most")

            elif sort == str(1):
                # prnt+=str(all_boycotts)
                all_boycotts=sorted(all_boycotts, key=sort_by_alpha)
                # prnt += '|'+str(all_boycotts)
                print("sorting by alpha")

            elif sort == str(3):
                all_boycotts=sorted(all_boycotts, key=sort_by_comments, reverse=True)
            print("all boycotts")
            print(all_boycotts)
            all_boycotts_json = json.loads(json.dumps(all_boycotts))
            # return HttpResponseRedirect('/?alert=signup')

            return render(request, 'home.html', {
                'alert': alert,
                'my_boycotts': my_boycotts_json,
                'trending_boycotts': trending_boycotts_json,
                'all_boycotts': json.loads(json.dumps(all_boycotts)),
                'filterForm': form,
                'news': news
            })

    else:
        form = FilterForm(initial={'tag': '1', 'sort': '1'})
        all_boycotts=[]
        for boycott in Boycotted.objects.all():
            zipcode = boycott.zip
            location = process_zip(zipcode)

            top_bct = {
                'name': boycott.name,
                'id': boycott.id,
                'num': boycott.boycotts.count(),
                'location': location
            }
            all_boycotts.append(top_bct)

        all_boycotts_json = json.loads(json.dumps(sorted(all_boycotts, key=sort_by_most, reverse=True)))
        # all_boycotts_json = json.loads(json.dumps([]))



    return render(request, 'home.html', {
        'alert': alert,
        'my_boycotts': my_boycotts_json,
        # 'top_boycotts': top_boycotts_json,
        'trending_boycotts': trending_boycotts_json,
        'all_boycotts': all_boycotts_json,
        'filterForm': form,
        'news': news,
        'print':prnt,
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


    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form})


def _get_disqus_sso(user):
    if user.is_authenticated():
        disqus_sso = get_disqus_sso(
            user.id,
            user.username,
            user.email, )
    else:
        disqus_sso = get_disqus_sso()
    return disqus_sso


def reset_password(request, token):
    token_obj = Token.objects.filter(token=token)
    if token_obj.count() == 0:
        token_obj = None
    else:
        token_obj = token_obj[0]
    if (token_obj is None) or (token_obj.date - datetime.datetime.now(datetime.timezone.utc) > TOKEN_EXPIRE):
        return HttpResponseRedirect('/?alert=expired')
    else:
        if request.method == 'POST':
            password_form = ResetPasswordForm(data=request.POST)
            if password_form.is_valid():
                # Save boycotted values to access
                user = token_obj.user
                user.set_password(password_form.save(commit=False).password)
                user.save()
                token_obj.delete()
                login(request, user)

                return HttpResponseRedirect('/?alert=password')

        else:
            password_form = ResetPasswordForm()

        return render(request, 'reset_password.html', {
            'password_form': password_form,
            'username': token_obj.user.username,
            'token': token
        })


def get_reset(request):
    if request.method == 'POST':
        token_form = TokenForm(data=request.POST)
        if token_form.is_valid():
            # process data in form
            cleanEmail = token_form.cleaned_data
            email = cleanEmail.get('email')
            user = BoycottUser.objects.get(email=email)
            token = token_generator()
            Token.objects.create(
                user=user,
                token=token
            )
            root=bct_settings.CURRENT_ROOT
            send_mail('Boycott Pal Password Recovery',
                      'Here is your password reset link: \n' + str(root) + 'reset/use/' + token,
                      'Boycott_Support@BoycottPal.com', [email],
                      fail_silently=False)

            return HttpResponseRedirect('/?alert=reset')


    else:
        token_form = TokenForm()

    return render(request, 'get_reset.html', {'token_form': token_form})

@login_required(login_url='/login/')
def change_password(request):
    email_form = ChangeEmailForm()
    if request.method == 'POST':
        password_form = ChangePasswordForm(data=request.POST, user=request.user)
        if password_form.is_valid():
            # process data in form


            password = password_form.cleaned_data.get('password')
            user = request.user
            user.set_password(password)
            user.save()
            if user is not None:
                login(request, user)

            return HttpResponseRedirect('/?alert=password')


    else:
        password_form = ChangePasswordForm()
        email_form = ChangeEmailForm()

    return render(request, 'settings.html', {
        'email_form': email_form,
        'password_form': password_form
    })

@login_required(login_url='/login/')
def change_email(request):
    password_form = ChangePasswordForm()
    if request.method == 'POST':
        email_form = ChangeEmailForm(data=request.POST, user=request.user)
        if email_form.is_valid():
            # process data in form


            email = email_form.save(commit=False).email
            user = request.user
            user.email = email
            user.save()

            return HttpResponseRedirect('/?alert=email')
    else:
        email_form = ChangeEmailForm()
        password_form = ChangePasswordForm()

    return render(request, 'settings.html', {
        'email_form': email_form,
        'password_form': password_form
    })

@login_required(login_url='/login/')
def settings(request):
    email_form = ChangeEmailForm()
    password_form = ChangePasswordForm()
    return render(request, 'settings.html', {
        'email_form': email_form,
        'password_form': password_form
    })

# @login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def Console(request):
    raw_alert = request.GET.get('alert')
    if raw_alert == None:
        alert = ""
    else:
        alert = raw_alert

    email_form = EmailForm()
    poll_form = NewPollForm()
    num_users=BoycottUser.objects.all().count()
    num_boycotts=Boycott.objects.all().count()
    num_hits=HC.objects.all()[0].hits

    return render(request, 'console.html', {
        'alert': alert,
        'email_form': email_form,
        'poll_form': poll_form,
        'num_users': num_users,
        'num_boycotts': num_boycotts,
        'num_hits': num_hits,
    })


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def MassEmail(request):
    raw_alert = request.GET.get('alert')
    if raw_alert == None:
        alert = ""
    else:
        alert = raw_alert
    if request.method == 'POST':
        email_form = EmailForm(data=request.POST)
        if email_form.is_valid():

            # process data in form
            cleanEmail = email_form.cleaned_data
            email = cleanEmail.get('email')
            subject = cleanEmail.get('subject')
            mailList = []
            for user in BoycottUser.objects.all():
                mailList.append(user.email)

            send_mail(subject, email, 'admin@BoycottPal.com', mailList,
                      fail_silently=True)
            return HttpResponseRedirect('/console/?alert=sent')

    else:
        email_form = EmailForm()
        alert=''

    return render(request, 'console.html', {
        'email_form': email_form,
        'alert': alert
    })

def Terms(request):
    return render(request, 'terms.html')
@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def ViewAllUsers(request):
    all_users=[]
    for user in BoycottUser.objects.all():
        usr= {
            'name':user.username,
            'email':user.email,
            'id':user.id,
            'location':process_zip(user.zip)
        }
        all_users.append(usr)

    return render(request, 'view_all_users.html', {
        'all_users': all_users
    })

@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def DeleteUser(request, user_id):
    user = BoycottUser.objects.get(id=user_id)

    user.delete()


    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def Blog(request):
    disqus_sso = _get_disqus_sso(request.user)
    return render(request, 'blog.html', {
        'disqus_sso':disqus_sso
    })