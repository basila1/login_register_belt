from __future__ import unicode_literals
from django.db import models
import bcrypt, re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
Name_Regex = re.compile (r'^[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):
    def register(self, postData):
        errors = []

        if len(postData['first_name']) < 2:
            errors.append('First Name must have at least 2 characters!')

        if len(postData['last_name']) < 2:
            errors.append('Last Name must have at least 2 characters')

        if not Name_Regex.match(postData['first_name']):
            errors.append("Must provide a valid first name!")

        if not Name_Regex.match(postData['last_name']):
            errors.append("Must provide a valid last name!")

        if not email_regex.match(postData['email']):
            errors.append('Not a valid email')

        if len(postData['email']) == 0:
            errors.append('Please enter an email')

        if postData['password'] != postData['confirm']:
            errors.append('Passwords do not match. Try again')

        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters')

        same = User.objects.filter(email=postData['email'])
        if same:
            errors.append('Email is already in use')

        if len(errors) == 0:
            pwHash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt().encode())
            user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=pwHash)
            return (True, user)

        else:
            return (False, errors)

    def login(self, postData):
        errors = []
        user = User.objects.filter(email=postData['email'])
        if user.exists():
            InputPw = postData['password'].encode()
            HashPw = user[0].password.encode()

            if bcrypt.checkpw(InputPw, HashPw):
                return (True, user[0])
            else:
                errors.append(("Email or password doesn't exist!"))
        else:
            errors.append(("Email or password doesn't exist!"))
        return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
