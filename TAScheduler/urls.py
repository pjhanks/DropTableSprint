from django.urls import path
from . import views
from django.contrib import admin
from TAScheduler.views import Login, Home, Instructors, Courses, TA

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('home/', views.homeView, name='home'),
    #path('', views.loginView, name='login'),
    #path('courses/', views.coursesView, name='courses'),
    #path('instructors/', views.instructorsView, name='instructors'),
    #path('TA/', views.taView, name='TA'),
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('home/', Home.as_view(), name='home'),
    path('instructors/', Instructors.as_view(), name='instructors'),
    path('TA/', TA.as_view(), name='TA'),
    path('courses/', Courses.as_view(), name='course'),

]
