from django.urls import path
from . import views
from django.contrib import admin
from TAScheduler.views import Login, Home, Users, Courses, \
    Section, makeUser, removeUser, makeCourse, removeCourse, makeSection, \
    removeSection, addInstructor, removeInstructor, addTA, removeTA1, removeTA2, addTAsec, addTAsec2, removeTAsec, \
    removeTAsec2, addTAsec3, editContactInfo,addSkills,addSkillSup



urlpatterns = [

    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('home/', Home.as_view(), name='home'),
    path('users/', Users.as_view(), name='users'),
    path('sections/', Section.as_view(), name='section'),
    path('courses/', Courses.as_view(), name='courses'),
    path('makeUser/', makeUser.as_view(), name='makeUser'),
    path('removeUser/', removeUser.as_view(), name='removeUser'),
    path('makeUser/', makeUser.as_view(), name='makeUser'),
    path('makeCourse/', makeCourse.as_view(), name='makeCourse'),
    path('removeCourse/', removeCourse.as_view(), name='removeCourse'),
    path('makeSection/', makeSection.as_view(), name='makeSection'),
    path('removeSection/', removeSection.as_view(), name='removeSection'),
    path('addInstructor/', addInstructor.as_view(), name='addInstructor'),
    path('addTA/', addTA.as_view(), name='addTA'),
    path('removeInstructor/', removeInstructor.as_view(), name="removeInstructor"),
    path('removeTA1/', removeTA1.as_view(), name="removeTA"),
    path('removeTA2/', removeTA2.as_view(), name="removeTA"),
    path('addTAsec2/', addTAsec2.as_view(), name="addTAsec2"),
    path('addTAsec3/', addTAsec3.as_view(), name="addTAsec3"),
    path('addTAsec/', addTAsec.as_view(), name="addTAsec"),
    path('removeTAsec/', removeTAsec.as_view(), name="removeTAsec"),
    path('removeTAsec2/', removeTAsec2.as_view(), name="removeTAsec2"),
    path('editContactInfo/',editContactInfo.as_view(), name="editContactInfo"),
    path('addSkills/', addSkills.as_view(), name="addSkills"),
    path('addSkillSup/',addSkillSup.as_view(), name ="addSkillSup")
]
