from django.contrib import admin
from .models import MyUser
from .models import Sections
from .models import ClassTAAssignments
from .models import Course
from .models import UserSkills
from .models import Skills

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Sections)
admin.site.register(ClassTAAssignments)
admin.site.register(Course)
admin.site.register(UserSkills)
admin.site.register(Skills)