from django.contrib import admin
from .models import MyUser, TA, Course, Sections, classTAAssignments
# Register your models here.
admin.site.register(MyUser)
admin.site.register(TA)
admin.site.register(Course)
admin.site.register(Sections)
admin.site.register(classTAAssignments)