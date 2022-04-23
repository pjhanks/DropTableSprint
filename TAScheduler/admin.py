from django.contrib import admin
from .models import MyUser
from .models import TA
from .models import Sections
from .models import classTAAssignments
from .models import Course

# Register your models here.
admin.site.register(MyUser)
admin.site.register(TA)
admin.site.register(Sections)
admin.site.register(classTAAssignments)
admin.site.register(Course)
