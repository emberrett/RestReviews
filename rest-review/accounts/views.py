from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'There is already an account with this email, please login.')
                return redirect(register)
            else:
                user = User.objects.create_user(username=email, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save()
                
                return redirect('login_user')


        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
            

    else:
        return render(request, 'accounts/registration.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Email or Password')
            return redirect('login_user')



    else:
        return render(request, 'accounts/login_user.html')


def logout_user(request):
    auth.logout(request)
    return redirect('home')