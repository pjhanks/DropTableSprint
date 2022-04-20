from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home, name='home'),
    path('courses/', views.Home.as_view())
]