from django.contrib import admin
from .models import ClassD, ClassM
from studyroom.models import Reserve

admin.site.register(ClassD)
admin.site.register(ClassM)
admin.site.register(Reserve)
# Register your models here.
