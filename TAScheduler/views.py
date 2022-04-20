from django.shortcuts import render, redirect
from django.views import View
from .models import MyUser
# Create your views here.
from django.http import HttpResponse

class Home(View):
    def get(self, request):
        return render(request, "home.html")

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = MyUser.objects.get(name=request.POST['name'])
            badPassword = (m.password != request.POST['password'])
        except:
            noSuchUser = True
        if noSuchUser:
            m = MyUser(name=request.POST['name'], password=request.POST['password'])
            m.save()
            request.session["name"] = m.name
            return redirect("/courses/")
        elif badPassword:
            return render(request, "home.html", {"message": "bad password"})
        else:
            request.session["name"] = m.name
            return redirect("/courses/")

    def myView(request):
         return render(request, "home.html", {})