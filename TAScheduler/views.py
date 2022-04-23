from django.shortcuts import render, redirect
from django.views import View
from .models import MyUser
import logging
# Create your views here.
from django.http import HttpResponse


class Login(View):

    # Put the logging info within your django view

    def get(self, request):
        logger = logging.getLogger(__name__)
        logger.info("Simple info")
        print("TEST")

        return render(request, "login.html")

    def post(self, request):
        noSuchUser = False
        blankName = False
        badPassword = False

        try:
            print(request.POST['InputUsername'])
            m = MyUser.objects.get(userID=request.POST['InputUsername'])
            badPassword = (m.password != request.POST['InputPassword'])
        except:
            noSuchUser = True

        if noSuchUser:
            return render(request, "login.html", {"message": "no user"})

        elif badPassword:
            return render(request, "login.html", {"message": "bad password"})
        else:
            request.session["username"] = m.userID
            request.session["name"] = m.name
            return redirect("/home/")

    


class Home(View):

    def get(self, request):
        #print(request.session["name"])
        return render(request, "home.html", {"name" : request.session["name"]})


class Courses(View):

    def get(self, request):
        return render(request, "courses.html", {"name" : request.session["name"]})


class Instructors(View):

    def get(self, request):
        return render(request, "instructors.html", {"name" : request.session["name"]})


class TA(View):

    def get(self, request):
        return render(request, "TA.html", {"name" : request.session["name"]})
