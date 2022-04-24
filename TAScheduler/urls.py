from django.urls import path
from . import views
from django.contrib import admin
from TAScheduler.views import Login, Home, Users, Courses, Section, makeUser

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('home/', Home.as_view(), name='home'),
    path('users/', Users.as_view(), name='users'),
    path('sections/', Section.as_view(), name='section'),
    path('courses/', Courses.as_view(), name='courses'),
    path('makeUser/', makeUser.as_view(), name='makeUser'),

]
