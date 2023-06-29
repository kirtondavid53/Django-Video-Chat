from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def index(request):
    curr_user = request.user
    if request.method == 'POST':
        if curr_user.is_authenticated:
            code = request.POST['code']
            return redirect('/room?roomID='+code)
        else:
            messages.info(request, "Please register or login to get started")
            return redirect('index')


    if request is not None:
        return render(request, 'index.html', {'user':curr_user})
    
    else:
        return render(request, 'index.html')
    

def login_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            
            login(request, user)
            messages.info(request, "You have successfully logged in")
            return redirect('/')

        else:
            messages.info(request, "Invalid Credentials")  
            return redirect('login')

    else:  
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2 :
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.warning(request, 'Username has already been used')
                return redirect('register')
            
            else:
                user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
                user.save()
                login(request, user)
                messages.info(request, "Your account has been successfully created")
                return redirect('index')
            
        else:
            messages.warning(request, 'Passwords are not the name')
            return redirect(request, 'register')
        
    else:

        return render(request ,'register.html')
    


def logout_view(request):
    logout(request)
    return redirect('index')

def video_call(request):
    if request.user.is_authenticated:
        return render(request, 'videochat.html',  {"name" : request.user.first_name+ " "+ request.user.last_name})
    else:
        messages.info(request, "Please login or register to get started")
        return redirect('index')
    
