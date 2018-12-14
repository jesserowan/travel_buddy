from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'travel_app/index.html')

def register(request):
    errors = User.objects.register(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], pw_hash=hash1.decode('utf-8'))
        request.session['user_id'] = User.objects.get(id=user.id).id
        return redirect('/success')

def login(request):
    errors = User.objects.login(request.POST)
    print(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(username=request.POST['login_username']).id
        return redirect('/success')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        planned_trips = User.objects.get(id=request.session['user_id']).trips_planned.all()
        joined_trips = User.objects.get(id=request.session['user_id']).trips.all().exclude(planned_by=User.objects.get(id=request.session['user_id']))
        other_trips = Trip.objects.exclude(travellers=User.objects.get(id=request.session['user_id'])).exclude(planned_by=User.objects.get(id=request.session['user_id'])).all()
        print(other_trips)
        context = {
            "user": user,
            "trips_planned": planned_trips,
            "trips_joined": joined_trips,
            "other_trips": other_trips
        }
        return render(request, 'travel_app/home.html', context)

def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        return render(request, 'travel_app/new.html')

def add(request):
    errors = Trip.objects.add_trip(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/new')
    else:
        user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], departure=request.POST['departure'], return_date=request.POST['return_date'], planned_by=user)
        request.session['trip_id'] = Trip.objects.get(id=trip.id).id
        
        return redirect(f'/show/{trip.id}')

def show(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.get(id=id)
        travellers = Trip.objects.get(id=id).travellers.all()
        context = {
            "id": id,
            "user": user,
            "trip": trip,
            "travellers": travellers
        }
        return render(request, 'travel_app/trip.html', context)

def join(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    user.trips.add(trip.id)
    user.save()
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')
