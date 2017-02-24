from django.shortcuts import render, redirect, HttpResponse
from ..login.models import User
from .models import Trip
from django.core.urlresolvers import reverse
from django.contrib import messages

# Create your views here.
#check if user in session. get that particular user so that their information can be displaced on the html page. need their first name, trip start_date, end_date and description.
#to delete your travel plan. data == trip.user
def index(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'data': user, #user data
            'trips': Trip.objects.all().filter(group=user), #user trip data
            'users': Trip.objects.all().exclude(group=user) #to get other peoples travel plans!!!
        }
        return render(request, 'travel_app/index.html', context)
    else:
        return redirect(reverse('login:index'))

def add(request):
    return render(request, 'travel_app/add.html')

#when you submit the add trip button this is where it goes. get the user id that's in session, passing a tuple from models.py. if true, message successfully added and redirect back to trave/index.html. else error message 'need to fill out form fields'. redirect to add trip page!!
def process(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        result = Trip.objects.addTrip(request.POST, user) #was the addTrip function from models.py sucessfull?
        if result[0] == True:
            messages.success(request, result[1])
            return redirect(reverse('travel:index'))
        else:
            for error in result[1]: #result[1] == errors from models.py tuple
                messages.error(request, error)
            return redirect(reverse('travel:add'))

#class Trip, every trip gets its own id. get the trip id. want to pass the trip information:  destination, plan, start_date, end_date. first_name is coming from the user which is a foreign key!!!!! trips.user.first_name
def destination(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    context = {
        'trips': trip, #trip information
        'group': trip.group.all() #one user can be in many groups. get all the users in the group column.
    }
    return render(request,'travel_app/destination.html', context)

#get the user thats in session. if the user was joined to the groups column in trips. flash success message. return to travel/index
def join(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    result = Trip.objects.joinTrip(trip_id, user)
    messages.success(request, result[1])
    return redirect(reverse('travel:index'))

#the user thats looged in needs to be able to delete ther trip. get the trip id and .delete it redirect to trave/index.
def delete(request, trip_id):
    Trip.objects.get(id=trip_id).delete()
    messages.success(request, "Successfully deleted")
    return redirect(reverse('travel:index'))

#to cancel a trip. get user id and trip id. to remove user from the group column in trip (trip.group.remove(user)). redirect to travel/index
def cancel(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    trip.group.remove(user)
    messages.success(request, "Trip cancelled.")
    return redirect(reverse('travel:index'))

#to logout, request.session.clear() to remove user from session. redirect to login page.
def logout(request):
    request.session.clear()
    return redirect(reverse('login:index'))
