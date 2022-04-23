from django.shortcuts import render, redirect
from django.views import View
from .models import MyUser, Course
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
        # print(request.session["name"])
        return render(request, "home.html", {"name": request.session["name"]})


class Courses(View):

    def get(self, request):
        m = MyUser.objects.get(userID=request.session["username"])

        if (m.role == "Supervisor"):
            c = Course.objects.all()
        else:
            c = Course.objects.filter(instructorID=request.session["username"])


        return render(request, "courses.html", {"name": request.session["name"], "courses": c})


class Instructors(View):

    def get(self, request):

        m = MyUser.objects.get(userID=request.session["username"])

        if (m.role == "Supervisor"):
            i = MyUser.objects.filter(role="Instructor")
        else:
            i = MyUser.objects.filter(userID=request.session["username"])


        return render(request, "users.html", {"name": request.session["name"], "instructors": i})


class TA(View):

    def get(self, request):
        return render(request, "TA.html", {"name": request.session["name"]})
