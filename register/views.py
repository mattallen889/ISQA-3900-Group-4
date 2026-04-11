from django.shortcuts import render, redirect
from shop.views import product_list
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register(request):
    return render(request, 'register.html', {'errorPresent': False})

def registerErrorHandle(request, regErrorID):
    errorDecodeDict = {0: 'Username is already used.',
                       1: 'Username is too long.',
                       2: 'First name is too long.',
                       3: 'Last name is too long.',
                       4: 'Email is too long.',
                       5: 'Passwords do not match.',
                       6: 'Not all fields are filled.'}

    return render(request, 'register.html', {'errorPresent': True, 'errorMsg': errorDecodeDict[regErrorID]})

def signup(request):
    if request.method == 'POST':
        # Constants (constants are placeholders now, I (Caeden) will update them later to fit the database)
        MAX_USERNAME_SIZE = 150
        MAX_FIRST_NAME_SIZE = 150
        MAX_LAST_NAME_SIZE = 150
        MAX_EMAIL_SIZE = 150

        # Check to see whether the username entered has already been taken
        userObject = None
        try:
            userObject = User.objects.get(username=request.POST['username'])
            return redirect('/register/registrationError/0')
        except:
            pass

        # Validate input sizes and types

        if (request.POST['username'] == '' or request.POST['first_name'] == '' or request.POST['last_name'] == '' or request.POST['email'] == '' or request.POST['password'] == '' or request.POST['password2'] == ''):
            return redirect('/register/registrationError/6')
        elif (len(request.POST['username']) > MAX_USERNAME_SIZE):
            return redirect('/register/registrationError/1')
        elif (len(request.POST['first_name']) > MAX_FIRST_NAME_SIZE):
            return redirect('/register/registrationError/2')
        elif (len(request.POST['last_name']) > MAX_LAST_NAME_SIZE):
            return redirect('/register/registrationError/3')
        elif (len(request.POST['email']) > MAX_EMAIL_SIZE):
            return redirect('/register/registrationError/4')
        else:
            pass

        # Validate that password entries match
        if (request.POST['password'] != request.POST['password2']):
            return redirect('/register/registrationError/5')

        # Create the user account
        userObject = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
        userObject.save()

        # Redirect to login page
        return redirect('/registration/login/')
    else:
        return redirect('/register/')