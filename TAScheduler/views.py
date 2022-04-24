from django.shortcuts import render, redirect
from django.views import View
from .models import MyUser, Course, Sections
import logging
from .Users import UserClass
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

        return render(request, "courseCreation/courses.html",
                      {"name": request.session["name"], "courses": c, "role": m.role})


class Users(View):

    def get(self, request):

        m = MyUser.objects.get(userID=request.session["username"])

        if (m.role == "Supervisor"):
            i = MyUser.objects.all()
        else:
            i = MyUser.objects.filter(userID=request.session["username"])

        return render(request, "userCreation/users.html",
                      {"name": request.session["name"], "instructors": i, "role": m.role})


class Section(View):

    def get(self, request):

        m = MyUser.objects.get(userID=request.session["username"])

        if (m.role == "Supervisor"):
            s = Sections.objects.all()
        else:
            s = MyUser.objects.filter(userID=request.session["username"])

        return render(request, "sectionCreation/sections.html",
                      {"name": request.session["name"], "sections": s, "role": m.role})


class makeUser(View):

    def get(self, request):

        m = MyUser.objects.get(userID=request.session["username"])

        return render(request, "userCreation/makeUser.html", {"name": request.session["name"], "role": m.role})

    def post(self, request):
        ID = request.POST['InputUserID']
        Name = request.POST['InputName']
        Address = request.POST['InputAddress']
        Email = request.POST['InputEmail']
        PhoneNumber = request.POST['InputPhoneNumber']
        Role = request.POST['InputRole']
        Password = request.POST['InputPassword']

        try:
            UserClass.createUser(self, ID, Name, Address, Email, PhoneNumber, Role, Password)
        except:
            return render(request, "userCreation/makeUser.html",
                          {"name": request.session["name"], "message": "UserID is aleady in the system"})

        return redirect("/users/")

class removeUser(View):

    def get(self, request):

        m = MyUser.objects.all()

        if m.count() > 0 :
            return render(request, "userCreation/removeUser.html", {"name": request.session["name"], "users": m})

        else:
            return render(request, "userCreation/users.html",
                          {"name": request.session["name"], "message" : "No users to remove"})




