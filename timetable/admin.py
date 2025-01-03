from django.contrib import admin
from .models import ClassD, ClassM
from studyroom.models import Reserve

class ClassDAdmin(admin.ModelAdmin):
  pass
  list_display=('subject','professor')

admin.site.register(ClassD, ClassDAdmin)
admin.site.register(ClassM)
admin.site.register(Reserve)
# Register your models here.
