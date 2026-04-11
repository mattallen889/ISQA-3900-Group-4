from django.shortcuts import render, redirect
from shop.views import product_list
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register(request):
    return render(request, 'register.html')

def signup(request):
    if request.method == 'POST':
        # Check to see whether the username entered has already been taken
        userObject = None
        try:
            userObject = User.objects.get(username=request.POST['username'])
            return redirect('/')
        except:
            pass

        # Validate input sizes and types


        # Validate that password entries match
        if (request.POST['password'] != request.POST['password2']):
            return redirect('/register/')

        # Create the user account
        userObject = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
        userObject.save()

        # Redirect to login page
        return redirect('/registration/login/')
    else:
        return redirect('/register/')