from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from .models import MyUser, Course, Sections
import logging
from .Users import UserClass
from .Courses import CoursesClass
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

            m = MyUser.objects.get(IDNumber=request.POST['InputUsername'])
            badPassword = (m.password != request.POST['InputPassword'])
        except:
            noSuchUser = True

        if noSuchUser:
            return render(request, "login.html", {"message": "no user"})

        elif badPassword:
            return render(request, "login.html", {"message": "bad password"})
        else:
            request.session["username"] = m.IDNumber
            request.session["name"] = m.name
            return redirect("/home/")


class Home(View):

    def get(self, request):
        # print(request.session["name"])
        return render(request, "home.html", {"name": request.session["name"]})


class Courses(View):

    def get(self, request):
        m = MyUser.objects.get(IDNumber=request.session["username"])

        if (m.role == "Supervisor"):
            c = Course.objects.all()
        else:
            c = Course.objects.filter(instructorID=request.session["username"])

        return render(request, "courseCreation/courses.html",
                      {"name": request.session["name"], "courses": c, "role": m.role})


class Users(View):

    def get(self, request):

        m = MyUser.objects.get(IDNumber=request.session["username"])

        if (m.role == "Supervisor"):
            i = MyUser.objects.all()
        else:
            i = MyUser.objects.filter(IDNumber=request.session["username"])

        return render(request, "userCreation/users.html",
                      {"name": request.session["name"], "instructors": i, "role": m.role})


class Section(View):

    def get(self, request):

        m = MyUser.objects.get(IDNumber=request.session["username"])

        if (m.role == "Supervisor"):
            s = Sections.objects.all()
        else:
            s = MyUser.objects.filter(IDNumber=request.session["username"])

        return render(request, "sectionCreation/sections.html",
                      {"name": request.session["name"], "sections": s, "role": m.role})


class makeUser(View):

    def get(self, request):

        m = MyUser.objects.get(IDNumber=request.session["username"])
        if (m.role == "Supervisor"):
            return render(request, "userCreation/makeUser.html", {"name": request.session["name"], "role": m.role})
        else:
            return redirect("/users/")

    def post(self, request):
        ID = str(request.POST['InputIDNumber'])
        Name = str(request.POST['InputName'])
        Address = str(request.POST['InputAddress'])
        Email = str(request.POST['InputEmail'])
        PhoneNumber = str(request.POST['InputPhoneNumber'])
        Role = str(request.POST['InputRole']).strip()
        Password = str(request.POST['InputPassword'])
        print(Role)
        try:
            UserClass.createUser(self, ID, Name, Address, Email, PhoneNumber, Role, Password)
        except Exception as e:
            print(e)
            return render(request, "userCreation/makeUser.html",
                          {"name": request.session["name"], "message": "IDNumber is aleady in the system"})

        return redirect("/users/")


class removeUser(View):

    def get(self, request):

        m = MyUser.objects.filter(~Q(IDNumber=request.session["username"]))
        j = MyUser.objects.get(IDNumber=request.session["username"])
        if (m.role == "Supervisor"):
            if m.count() > 0:
                return render(request, "userCreation/removeUser.html", {"name": request.session["name"], "users": m})

            else:
                m = MyUser.objects.all()
                return render(request, "userCreation/users.html",
                              {"name": request.session["name"], "message": "No users to remove", "instructors": m,
                               "role": j.role})
        else:
            return redirect("/users/")

    def post(self, request):

        m = MyUser.objects.get(IDNumber=request.POST["InputUser"])
        m.delete()
        j = MyUser.objects.filter(~Q(IDNumber=request.session["username"]))
        return render(request, "userCreation/removeUser.html",
                      {"name": request.session["name"], "message": "User successfully removed", "users": j})


class makeCourse(View):

    def get(self, request):

        m = MyUser.objects.get(IDNumber=request.session["username"])
        j = MyUser.objects.filter(role="Instructor")
        if (m.role == "Supervisor"):
            return render(request, "courseCreation/makeCourse.html",
                          {"name": request.session["name"], "role": m.role, "users": j})
        else:
            return redirect("/courses/")

    def post(self, request):

        ID = request.POST['InputInstructor']
        CourseCode = request.POST['InputCourseCode']
        CourseNumber = request.POST['InputCourseNumber']
        j = MyUser.objects.filter(role="Instructor")

        if (ID == ''):
            try:
                CoursesClass.createCourseNoInstructor(self, CourseCode, CourseNumber)
            except Exception as e:

                return render(request, "courseCreation/makeCourse.html",
                              {"name": request.session["name"], "message": "Course Code is already in the system",
                               "users": j})
        else:
            x = str(ID).split("|")
            print(x[0])

            try:
                CoursesClass.createCourse(self, CourseCode, (x[0]).strip(), CourseNumber)
            except Exception as e:
                print(e)
                return render(request, "courseCreation/makeCourse.html",
                              {"name": request.session["name"], "message": "IDNumber is already in the system",
                               "users": j})

        return redirect("/courses/")


class removeCourse(View):

    def get(self, request):

        m = Course.objects.all()
        j = MyUser.objects.get(IDNumber=request.session["username"])
        if (m.role == "Supervisor"):
            if m.count() > 0:
                return render(request, "courseCreation/removeCourse.html",
                              {"name": request.session["name"], "courses": m})

            else:
                m = MyUser.objects.all()
                return render(request, "courseCreation/courses.html",
                              {"name": request.session["name"], "message": "No users to remove", "instructors": m,
                               "role": j.role})
        else:
            return redirect("/courses/")

    def post(self, request):

        m = Course.objects.get(courseCode=request.POST["InputCourse"])
        m.delete()
        j = Course.objects.all()
        return render(request, "courseCreation/removeCourse.html",
                      {"name": request.session["name"], "message": "User successfully removed", "courses": j})


class makeSection(View):

    def get(self, request):

        m = MyUser.objects.get(IDNumber=request.session["username"])
        j = Course.objects.all()

        x = Sections.objects.all()

        for sect in x:
            n = Course.objects.get(courseCode=sect.parentCode)

        if (m.role == "Supervisor"):
            return render(request, "courseCreation/makeCourse.html",
                          {"name": request.session["name"], "role": m.role, "users": j})
        else:
            return redirect("/sections/")

    def post(self, request):

        ID = request.POST['InputInstructor']
        CourseCode = request.POST['InputCourseCode']
        CourseNumber = request.POST['InputCourseNumber']
        j = MyUser.objects.filter(role="Instructor")

        if (ID == ''):
            try:
                CoursesClass.createCourseNoInstructor(self, CourseCode, CourseNumber)
            except Exception as e:

                return render(request, "courseCreation/makeCourse.html",
                              {"name": request.session["name"], "message": "Course Code is already in the system",
                               "users": j})
        else:
            x = str(ID).split("|")
            print(x[0])

            try:
                CoursesClass.createCourse(self, CourseCode, (x[0]).strip(), CourseNumber)
            except Exception as e:
                print(e)
                return render(request, "courseCreation/makeCourse.html",
                              {"name": request.session["name"], "message": "IDNumber is already in the system",
                               "users": j})

        return redirect("/courses/")
