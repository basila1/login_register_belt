from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from ..login.models import User

# Create your models here.
class TripManager(models.Manager):
    def addTrip(self, postData, user):
        print 'made it to addTrip'
        errors = []
#if all fields are empty (length == 0). error message!!!
        if len(postData['destination']) == 0 or len(postData['plan']) == 0 or len(postData['start_date']) == 0 or len(postData['end_date']) == 0:
            errors.append('Please fill out all fields of the form!')
#if start date and end date were entered (length > 0) use datetime.strptime(y,m,d). check time display assidgnment for syntax!!!
        if len(postData['start_date']) > 0 or len(postData['end_date']) > 0:
            start_date = datetime.strptime(postData['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(postData['end_date'], "%Y-%m-%d")

            # if datetime.today() >= start_date:
            #     errors.append('Start date must be in the future')
            # if start_date > end_date:
            #     errors.append('End date can not be before start date')

#if the errors array is empty, create the trip; destination, plan, user, start_date and end_date. and add the user to the groups column in trips.
        if len(errors) == 0:
            trip = Trip.objects.create(destination=postData['destination'], plan=postData['plan'], user=user, start_date=start_date, end_date=end_date)
            print 'trip was created'
            trip.group.add(user)
            print trip
            return (True, 'Successfully added trip to your schedule!')

        else:
            print 'made it to info not filled out for add trip'
            return (False, errors)

#join trip. adding a user to a group. Get the user and trip id??? go to the trips table, the group column and add the user. (Trip.group.add(user)). add the user in session to the trip id.....
    def joinTrip(self, trip_id, user):
        print 'made it to joinTrip'
        trip = Trip.objects.get(id=trip_id)
        trip.group.add(user)
        print trip
        return (True, "Successfully added trip to your schedule!")

#foreign key = user
#many to many = with groups. on trip can have many groups.
class Trip(models.Model):
    destination = models.CharField(max_length=50)
    plan = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User)
    group = models.ManyToManyField(User, related_name='travel')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
