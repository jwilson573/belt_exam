from django.shortcuts import render, redirect, reverse
from .models import User, Trip
from django.contrib import messages
from django.db.models import Count

def errorMessage(request, errors):
    for error in errors:
        messages.error(request, error)

def currentUser(request):
    user_id = request.session['user_id']
    return User.objects.get(id=user_id)

def index(request):
    
    return render(request, "belt_exam_app/index.html")


def create_user(request):
    
    if request.method == 'POST':
        
        form_valid = User.objects.validate(request.POST)

        if form_valid == []:

            user = User.objects.register(request.POST)

            request.session['user_id'] = user.id
            
            return render(request, "belt_exam_app/travelplans.html")

        errorMessage(request, form_valid)
        
        return redirect('/')

def logout(request):
    request.session.pop('user_id')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        
        data_check = User.objects.validate_login(request.POST)
        print data_check
        if type(data_check) == type(User()):

            request.session['user_id'] = data_check.id

            return redirect('/travels')
        
        errorMessage(request, data_check)

        return redirect('/')

def travels(request):
    print "Inside the travels method"
    current_user = currentUser(request)
    users = User.objects.all()
    all_trips = Trip.objects.all()
    my_trips = all_trips.filter(owner__id=current_user.id)
    other_trips = Trip.objects.all().exclude(owner=current_user)
    
    content = {
        'trips': all_trips,
        'user': current_user,
        'other_trips': other_trips,
        'my_trips': my_trips,
        'users': users
    }

    
    

    return render(request, "belt_exam_app/travelplans.html", content)

def add_trip(request):
    print "Inside the add_trip method."

    user = currentUser(request)
    

    return render(request, "belt_exam_app/addtrip.html")

def create_trip(request):
    print "Inside the create_trip method"

    if request.method == 'POST':
        user = currentUser(request)
        trip = Trip.objects.create_trip(user, request.POST)
        
    return redirect('/travels')


def join_trip(request, id):
    print "Inside the join_trip method"
    user = currentUser(request)
    trip = Trip.objects.get(id=id)

    user.created_trips.add(trip)

    return redirect('/travels')

def view_dest(request, id):

    current_user = currentUser(request)
    other_users = User.objects.all().exclude(id=current_user.id)
    users = User.objects.all()
    all_trips = Trip.objects.all()
    my_trips = all_trips.filter(owner__id=current_user.id)
    other_trips = Trip.objects.all().exclude(owner=current_user)
    current_trip = Trip.objects.get(id=id)
    
    content = {
        'trips': all_trips,
        'user': current_user,
        'other_trips': other_trips,
        'my_trips': my_trips,
        'users': users,
        'current_trip': current_trip,
        'other_users': other_users
    }

    return render(request,"belt_exam_app/destination.html", content)