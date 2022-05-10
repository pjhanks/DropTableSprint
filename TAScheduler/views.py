from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from .models import MyUser, Course, Sections, UserSkills, Skills
import logging
from TAScheduler.classes.Users import UserClass
from TAScheduler.classes.Courses import CoursesClass
from TAScheduler.classes.Sections import SectionsClass


# Create your views here.


class Login(View):

    # Put the logging info within your django view

    def get(self, request):
        logger = logging.getLogger(__name__)
        logger.info("Simple info")

        return render(request, "login.html")

    def post(self, request):
        noSuchUser = False
        blankName = False
        badPassword = False

        try:

            user = MyUser.objects.get(IDNumber=request.POST['InputUsername'])
            badPassword = (user.password != request.POST['InputPassword'])
        except:
            noSuchUser = True

        if noSuchUser:
            return render(request, "login.html", {"message": "no user"})

        elif badPassword:
            return render(request, "login.html", {"message": "bad password"})
        else:
            request.session["username"] = user.IDNumber
            request.session["name"] = user.name
            return redirect("/home/")


class Home(View):

    def get(self, request):
        return render(request, "home.html", {"name": request.session["name"]})


class Courses(View):

    def get(self, request):
        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        sectionDict = dict()

        if (loggedUser.role == "Supervisor"):
            allCourses = Course.objects.all()



        else:
            allCourses = Course.objects.filter(instructorID=request.session["username"])


        for x in allCourses:
            j = (list(Sections.objects.filter(parentCode=x.courseCode).values_list('sectionCode')))
            i = " | ".join([x[0] for x in j])
            sectionDict[x.courseCode] = i


        return render(request, "courseTemplates/courses.html",
                      {"name": request.session["name"], "courses": allCourses, "role": loggedUser.role, "sections": sectionDict})



class Users(View):

    def get(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        skillDict = dict()

        if (loggedUser.role == "Supervisor"):
            allUsers = MyUser.objects.all()
        else:
            allUsers = MyUser.objects.filter(IDNumber=request.session["username"])

        for x in allUsers:
            j = (list(UserSkills.objects.filter(UserID=x.IDNumber)))
            skillString=""
            for i in j:
                skillString = skillString + ( i.SkillID.SkillDescription ) + ", "
            skillDict[x.IDNumber] = skillString



        return render(request, "userTemplates/users.html",
                      {"name": request.session["name"], "instructors": allUsers, "role": loggedUser.role, "skills" : skillDict})


class Section(View):

    def get(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        allSections = Sections.objects.none();

        if (loggedUser.role == "Supervisor"):
            allSections = Sections.objects.all()
        else:
            allCourses = Course.objects.filter(instructorID=request.session["username"])

            courseIDs = [Course.courseCode for Course in allCourses]
            allSections =  Sections.objects.filter(parentCode__in=courseIDs)

        print(allSections)
        return render(request, "sectionTemplates/sections.html",
                      {"name": request.session["name"], "sections": allSections, "role": loggedUser.role})


class makeUser(View):

    def get(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        if (loggedUser.role == "Supervisor"):
            return render(request, "userTemplates/makeUser.html",
                          {"name": request.session["name"], "role": loggedUser.role})
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

        try:
            UserClass.createUser(self, ID, Name, Address, Email, PhoneNumber, Role, Password)
        except:

            return render(request, "userTemplates/makeUser.html",
                          {"name": request.session["name"], "message": "ID Number is already in the system"})

        return redirect("/users/")


class removeUser(View):

    def get(self, request):

        allUserWithoutLoggedUser = MyUser.objects.filter(~Q(IDNumber=request.session["username"]))
        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        if (loggedUser.role == "Supervisor"):
            if allUserWithoutLoggedUser.count() > 0:
                return render(request, "userTemplates/removeUser.html",
                              {"name": request.session["name"], "users": allUserWithoutLoggedUser})

            else:
                allUserWithoutLoggedUser = MyUser.objects.all()
                return render(request, "userTemplates/users.html",
                              {"name": request.session["name"], "message": "No users to remove",
                               "instructors": allUserWithoutLoggedUser,
                               "role": loggedUser.role})
        else:
            return redirect("/users/")

    def post(self, request):

        userToRemove = MyUser.objects.get(IDNumber=request.POST["InputUser"])
        userToRemove.delete()
        allUserWithoutLoggedUser = MyUser.objects.filter(~Q(IDNumber=request.session["username"]))
        return render(request, "userTemplates/removeUser.html",
                      {"name": request.session["name"], "message": "User successfully removed",
                       "users": allUserWithoutLoggedUser})


class makeCourse(View):

    def get(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        allInstructors = MyUser.objects.filter(role="Instructor")
        if (loggedUser.role == "Supervisor"):
            return render(request, "courseTemplates/makeCourse.html",
                          {"name": request.session["name"], "role": loggedUser.role, "users": allInstructors})
        else:
            return redirect("/courses/")

    def post(self, request):

        ID = request.POST['InputInstructor']
        CourseCode = request.POST['InputCourseCode']
        CourseNumber = request.POST['InputCourseNumber']
        allInstructors = MyUser.objects.filter(role="Instructor")

        if (ID == ''):
            try:
                CoursesClass.createCourseNoInstructor(self, CourseCode, CourseNumber)
            except Exception as e:

                return render(request, "courseTemplates/makeCourse.html",
                              {"name": request.session["name"], "message": "Course Code is already in the system",
                               "users": allInstructors})
        else:
            x = str(ID).split("|")

            try:
                CoursesClass.createCourse(self, CourseCode, (x[0]).strip(), CourseNumber)
            except Exception as e:

                return render(request, "courseTemplates/makeCourse.html",
                              {"name": request.session["name"], "message": "IDNumber is already in the system",
                               "users": allInstructors})

        return redirect("/courses/")


class removeCourse(View):

    def get(self, request):

        allCourses = Course.objects.all()
        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        if (loggedUser.role == "Supervisor"):
            if allCourses.count() > 0:
                return render(request, "courseTemplates/removeCourse.html",
                              {"name": request.session["name"], "courses": allCourses})

            else:
                allCourses = MyUser.objects.all()
                return render(request, "courseTemplates/courses.html",
                              {"name": request.session["name"], "message": "No users to remove",
                               "instructors": allCourses,
                               "role": loggedUser.role})
        else:
            return redirect("/courses/")

    def post(self, request):

        courseToRemove = Course.objects.get(courseCode=request.POST["InputCourse"])
        courseToRemove.delete()
        allCourses = Course.objects.all()
        return render(request, "courseTemplates/removeCourse.html",
                      {"name": request.session["name"], "message": "Course successfully removed",
                       "courses": allCourses})


class makeSection(View):

    def get(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        allCourses = Course.objects.all()

        if (loggedUser.role == "Supervisor"):
            return render(request, "sectionTemplates/makeSection.html",
                          {"name": request.session["name"], "role": loggedUser.role, "courses": allCourses})
        else:
            return redirect("/sections/")

    def post(self, request):

        InputSectionCode = request.POST['InputSectionCode']
        InputCourse = request.POST['InputCourse']
        allCourses = Course.objects.all()

        x = str(InputCourse).split("|")

        sectionCode = (x[1].strip() + "-" + InputSectionCode)

        try:
            SectionsClass.createSection(self, sectionCode, x[0].strip())
        except Exception as e:

            return render(request, "sectionTemplates/makeSection.html",
                          {"name": request.session["name"], "message": "IDNumber is already in the system",
                           "courses": allCourses})

        return redirect("/sections/")


class removeSection(View):

    def get(self, request):

        allSections = Sections.objects.all()
        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])

        if (loggedUser.role == "Supervisor"):
            if allSections.count() > 0:
                return render(request, "sectionTemplates/removeSection.html",
                              {"name": request.session["name"], "sections": allSections})

            else:
                allSections = MyUser.objects.all()
                return render(request, "sectionTemplates/sections.html",
                              {"name": request.session["name"], "message": "No Sections to remove",
                               "sections": allSections,
                               "role": loggedUser.role})
        else:
            return redirect("/section/")

    def post(self, request):

        sectionToDelete = Sections.objects.get(sectionCode=request.POST["InputCourse"])
        sectionToDelete.delete()
        allSections = Sections.objects.all()
        return render(request, "sectionTemplates/removeSection.html",
                      {"name": request.session["name"], "message": "Section successfully removed",
                       "sections": allSections})


class addInstructor(View):

    def get(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        coursesNoInstructor = Course.objects.filter(instructorID=None)
        allInstructors = MyUser.objects.filter(role="Instructor")

        return render(request, "courseTemplates/addInstructor.html",
                      {"name": request.session["name"], "courses": coursesNoInstructor, "users": allInstructors})

    def post(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        coursesNoInstructor = Course.objects.filter(instructorID=None)
        allInstructors = MyUser.objects.filter(role="Instructor")

        courseCode = (str(request.POST["InputCourse"]).split("|"))[0].strip()
        instructorID = (str(request.POST["InputInstructor"]).split("|"))[0].strip()

        try:
            CoursesClass.assignInstructor(self, courseCode, instructorID)
            allCourses = Course.objects.all()
            return render(request, "courseTemplates/courses.html",
                          {"name": request.session["name"], "courses": allCourses, "role": loggedUser.role})

        except Exception as e:
            print(e)
            return render(request, "courseTemplates/addInstructor.html",
                          {"name": request.session["name"], "courses": coursesNoInstructor, "users": allInstructors,
                           "message": "Could not add instructor"})

class removeInstructor(View):
    def get(self, request):

        allCourses = Course.objects.all()
        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])

        if (loggedUser.role == "Supervisor" or loggedUser.role == "Instructor"):
            if allCourses.count() > 0:
                return render(request, "courseTemplates/removeInstructor.html",
                              {"name": request.session["name"], "courses": allCourses})

            else:
                allCourses = MyUser.objects.all()
                return render(request, "courseTemplates/courses.html",
                              {"name": request.session["name"], "message": "No Courses to remove the instructor from",
                               "courses": allCourses,
                               "role": loggedUser.role})
        else:
            return redirect("/courses/")

    def post(self, request):
        courseCode = (str(request.POST["InputCourse"]).split("|"))[0].strip()

        CoursesClass.removeInstructor(self, courseCode)
        allCourses = Course.objects.all()
        return render(request, "courseTemplates/removeInstructor.html",
                      {"name": request.session["name"], "message": "Instructor successfully removed",
                       "courses": allCourses})

class addTA(View):

    def get(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        courses = Course.objects.all()
        allTAs = MyUser.objects.filter(role="TA")

        return render(request, "courseTemplates/addTA.html",
                      {"name": request.session["name"], "courses": courses, "users": allTAs})

    def post(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        courses = Course.objects.all()
        allTAs = MyUser.objects.filter(role="TA")

        courseCode = (str(request.POST["InputCourse"]).split("|"))[0].strip()
        TAcode = (str(request.POST["InputTA"]).split("|"))[0].strip()

        try:
            CoursesClass.assignTA(self, courseCode, TAcode)
            allCourses = Course.objects.all()
            return render(request, "courseTemplates/courses.html",
                          {"name": request.session["name"], "courses": allCourses, "role": loggedUser.role})

        except Exception as e:

            return render(request, "courseTemplates/addTA.html",
                          {"name": request.session["name"], "courses": courses, "users": allTAs,
                           "message": "Could not add TA"})

class removeTA(View):

    def get(self, request):
        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        courses = Course.objects.all()
        allTAs = MyUser.objects.filter(role="TA")

        return render(request, "courseTemplates/removeTA.html",
                      {"name": request.session["name"], "courses": courses, "users": allTAs})

    def post(self, request):
        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        courses = Course.objects.all()
        allTAs = MyUser.objects.filter(role="TA")

        courseCode = (str(request.POST["InputCourse"]).split("|"))[0].strip()
        TAcode = (str(request.POST["InputTA"]).split("|"))[0].strip()

        try:
            CoursesClass.assignTA(self, courseCode, TAcode)
            allCourses = Course.objects.all()
            return render(request, "courseTemplates/courses.html",
                          {"name": request.session["name"], "courses": allCourses, "role": loggedUser.role})

        except Exception as e:
            print(e)
            return render(request, "courseTemplates/removeTA.html",
                          {"name": request.session["name"], "courses": courses, "users": allTAs,
                           "message": "Could not remove TA"})

class addTAsec(View):

    def get(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        sections = Sections.objects.all()
        allTAs = MyUser.objects.filter(role="TA")

        return render(request, "sectionTemplates/addTAsec.html",
                      {"name": request.session["name"], "sections": sections, "users": allTAs})

    def post(self, request):

        loggedUser = MyUser.objects.get(IDNumber=request.session["username"])
        sections = Sections.objects.all()
        allTAs = MyUser.objects.filter(role="TA")

        sectionCode = (str(request.POST["InputSec"]).split("|"))[0].strip()
        TAcode = (str(request.POST["InputTA"]).split("|"))[0].strip()

        try:
            SectionsClass.assignTAsec(self, sectionCode, TAcode)
            allSections = Sections.objects.all()
            return render(request, "sectionTemplates/addTAsec.html",
                          {"name": request.session["name"], "sections": allSections, "role": loggedUser.role})

        except Exception as e:
            print(e)
            return render(request, "sectionTemplates/addTAsec.html",
                          {"name": request.session["name"], "sections": sections, "users": allTAs,
                           "message": "Could not add TA"})