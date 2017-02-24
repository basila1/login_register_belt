from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User

# Create your views here.

def index(request):
    return render(request, 'login/index.html')

def register(request):
    user = User.objects.validateRegister(request.POST)
    if user[0] == False:
        for error in user[1]:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['id'] = user[1].id
        print "Welcome User", request.session['id']
        context = {
        'users': User.objects.get(email=request.POST['email'])
        }
        return redirect("/success")

def login(request):
    user = User.objects.loginValidate(request.POST)
    if user[0] == False:
        for error in user[1]:
            messages.error(request, error)
        return redirect('/')
    else:
        print "We made it"
        if 'id' not in request.session:
            request.session['id'] = user[1].id
        print "got session", request.session['id']
        context = {
        'users': User.objects.get(email=request.POST['email'])
        }
        return redirect("/success")

def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
    'users': user
    # 'posts': Post.objects.all(),
    # 'posts': Post.objects.annotate(num_likes=Count('likes'))
    }
    return render(request, 'login/home_page.html', context)


def logout(request):
    request.session.pop('id')
    return render(request, 'login/index.html')
