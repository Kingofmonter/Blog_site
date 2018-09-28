from django.shortcuts import render,HttpResponse,redirect

# Create your views here.


def login(requset):


    return render(requset,'login.html')