from django.shortcuts import render,redirect,get_list_or_404, get_object_or_404
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from django.contrib import messages
# from mrbot.models import Exam
from time import sleep
from django.core.mail import send_mail,BadHeaderError
# from placementbot.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD
# from mrbot.models import pin
# Create your views here.

def logout(request):
    sleep(5)
    auth.logout(request)
    return render(request,'thanks.html')

def login(request):
    # if request.user:
    #     return redirect('field-choice')
    if request.method == "POST":

        username = request.POST['email']
        password = request.POST['psw']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
                auth.login(request,user)
                return redirect('field-choice')
        else:
            messages.info(request,'invalid cradentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method=="POST":
        first_name=request.POST['fname']
        last_name = request.POST['lname']
        tech=request.POST['tech']
        email = request.POST['email']
        username = request.POST['email']
        password1 = request.POST['psw']
        password2 = request.POST['psw-repeat']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password1)

                user.save()
                messages.info(request, 'Registration successful. Please check your mail to know your chat_id')
                return render(request,'login.html',{'color':'green'})

        else:
            messages.info(request,'Password not match')
            return redirect('login')
    else:
        return render(request,'login.html')