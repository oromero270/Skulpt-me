from django.shortcuts import render, HttpResponse, redirect
from . models import *
from django.contrib import messages
import bcrypt
import time
from django.db.models import Max
from django.db.models import Q


def index(request):
    return render(request,"landing.html")

def myhome(request):
    if 'loggedinId' not in request.session:
        return redirect ('/')
    else:
        activeuser = users.objects.get(id=request.session['loggedinId'])
        context= {
            'myinfo':activeuser,
        }
        return render (request, 'myhome.html', context)

def first_test (request):
    if 'loggedinId' not in request.session:
        return redirect ('/')
    else:
        activeuser = users.objects.get(id=request.session['loggedinId'])
        context= {
            'myinfo':activeuser,
        }
    return render (request, 'first_test.html',context)

def second_test (request):
    if 'loggedinId' not in request.session:
        return redirect ('/')
    else:
        activeuser = users.objects.get(id=request.session['loggedinId'])
        count=request.session['situps']
        context= {
            'myinfo':activeuser,
            'count':count
        }
    return render (request, 'second_test.html',context)

def third_test (request):
    if 'loggedinId' not in request.session:
        return redirect ('/')
    else:
        activeuser = users.objects.get(id=request.session['loggedinId'])
        count=request.session['situps']
        count2=request.session['pushups']
        context= {
            'myinfo':activeuser,
            'count':count,
            'count2':count2
        }
    return render (request, 'third_test.html',context)

def final_test (request):
    if 'loggedinId' not in request.session:
        return redirect ('/')
    else:
        activeuser = users.objects.get(id=request.session['loggedinId'])
        count=request.session['situps']
        count2=request.session['pushups']
        time=request.session['planked']
        context= {
            'myinfo':activeuser,
            'count':count,
            'count2':count2,
            'time':time
            
        }
    return render (request, 'final_test.html',context)

def first_sub (request):
    request.session['situps']=request.POST['sittest']
    return redirect ('/test2')
def second_sub (request):
    request.session['pushups']=request.POST['pushtest']
    return redirect ('/test3')
def third_sub (request):
    request.session['planked']=request.POST['planktest']
    return redirect ('/test4')
def final_sub (request):
    workdone=fitness.objects.create(situps = request.session['situps'], pushups =request.session['pushups'], plank_time=request.session['planked'], squats= request.POST['squattest'])
    workdoneid=fitness.objects.get(id=workdone.id)
    activeuser = users.objects.get(id=request.session['loggedinId'])
    workdoneid.userfitness.add(activeuser)
    return redirect ('/home')

def examnotes(request):
    if 'loggedinId' not in request.session:
        return redirect ('/')
    else:
        activeuser = users.objects.get(id=request.session['loggedinId'])
        sit=activeuser.myfitness.all().aggregate(maxsits=Max('situps'))
        sit['maxsits']
        push=activeuser.myfitness.all().aggregate(maxpush=Max('pushups'))
        push['maxpush']
        plank=activeuser.myfitness.all().aggregate(maxplank=Max('plank_time'))
        plank['maxplank']
        squat=activeuser.myfitness.all().aggregate(maxsquat=Max('squats'))
        squat['maxsquat']

        context= {
            'myinfo':activeuser,
            'fit':sit['maxsits'],
            'push':push['maxpush'],
            'plank':plank['maxplank'],
            'squat':squat['maxsquat'],
        }
    return render (request,'pretest.html', context)

def history (request):
    activeuser = users.objects.get(id=request.session['loggedinId'])
    fit=activeuser.myfitness.all()
    context={
        'info':fit
    }
    return render (request,'stats.html', context)

def creating (request):
    errorsmade = users.objects.basic_validator(request.POST)
    if len(errorsmade) > 0 :
        for key, value in errorsmade.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pwhash=bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        account =users.objects.create(first_name = request.POST['fname'],last_name = request.POST['lname'], email = request.POST['mail'],username =request.POST['acctname'] , password = pwhash)
        request.session['loggedinId'] = account.id
        return redirect ('/home')

def security (request):
    errorsmade = users.objects.login_validator(request.POST)
    if len(errorsmade) > 0 :
        for key, value in errorsmade.items():
            messages.error(request, value)
        return redirect(f'/')
    else:
        account=users.objects.get(username = request.POST['acctname'])
        request.session['loggedinId'] = account.id
        return redirect ('/home')


def prework(request):

    return render (request, 'pre_workout.html')

def sub_today_workout (request):
    workouts=[]
    for g in request.POST['gear']:
        workouts.append(workout.objects.filter(Q(gear= g) | Q(focus =request.POST['focus']) | Q(difficulty =request.POST['difficulty'])))
    return redirect ('/work')

def begin_workout(request):
    
    

    return render (request,'start_workout.html')

def clearuser (request):
    request.session.clear()
    return redirect ('/')

def regval (request):
    av=request.POST['acctname']
    unamelist=users.objects.filter(username=av)
    if len (unamelist)> 0:
        found = True
    else:
        found = False
    context = {
        'found': found
    }

    return render (request,'regpartial.html', context)


    # filter through gear that match the post request comination plus the focus and difuicty 
    # gear from post will be a list 
def add_workout(request):
    return render (request, 'add.html')

def log_new_workout(request):
    workout.objects.create(name = request.POST['wname'],gear = request.POST['gear'], focus=request.POST['focus'], difficulty = request.POST['difficulty'])

    return redirect ('/add/workout')