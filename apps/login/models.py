from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

Email_Regex = re.compile (r'^[a-zA-Z0-9.+_]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')
Name_Regex = re.compile (r'^[a-zA-Z]+$')

class Manager(models.Manager):
    def validateRegister(self, postData):
        status = True
        errorlist = []
        if not Name_Regex.match(postData['first_name']):
            errorlist.append("Must provide valid first name!")
            status = False
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errorlist.append("Name must have at least 2 letters!")
            status = False
        if not Name_Regex.match(postData['last_name']):
            errorlist.append("Must provide valid last name!")
            status = False
        if not Email_Regex.match(postData['email']):
            errorlist.append("Must provide a valid email!")
            status = False
        if len(postData['password']) < 8:
            errorlist.append("Password must be at least 8 characters!")
            status = False
        if postData['password'] != postData['confirm']:
            errorlist.append("Passwords must match!")
            status = False
        if len(User.objects.filter(email=postData['email'])) > 0:
            errorlist.append("Email is already registered!")
            status = False
        if status == False:
            return (False, errorlist)
        else:
            password = postData['password']
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            newuser = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashed)
            return (True, newuser)

    def loginValidate(self, postData):
        olduser = User.objects.filter(email=postData['email'])
        status = True
        errorlist = []
        if len(olduser) < 1:
            errorlist.append("Must register!")
            status = False
        if len(postData['email']) < 1:
            errorlist.append("Must provide a valid email!")
            status = False
        if len(postData['password']) < 1:
            errorlist.append("Must provide a valid password")
            status = False
        if status == False:
            return (False, errorlist)
        else:
            if bcrypt.hashpw(postData['password'].encode(), olduser[0].password.encode()) == olduser[0].password:
                return (True, olduser[0])
            else:
                errorlist.append("Incorrect Password")
                return (False, errorlist)

    # def addInterest(self, postData):
    #     if not Name_Regex.match(postData['interest']):
    #         status = False
    #     if status == False:
    #         return errorlist
    #     else:
    #         Interest.objects.create(interest_name=request.POST['interest'])
    #         interest = Interest.objects.filter(request.POST['interest'])
    #         interest.objects.users.add(user)
    #         return True


class User(models.Model):
    objects = Manager()
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
