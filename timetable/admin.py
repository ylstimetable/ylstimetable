from django.contrib import admin
from .models import ClassD, ClassM
from studyroom.models import Reserve

class ClassDAdmin(admin.ModelAdmin):
  pass
  list_display=('title','professor','time','room')

class ReserveAdmin(admin.ModelAdmin):
  pass
  list_display=('room','reserved_day')
  def reserved_day(self, obj):
    return "{}-{}-{}".format(obj.year,obj.month,obj.day)
  

admin.site.register(ClassD, ClassDAdmin)
admin.site.register(ClassM)
admin.site.register(Reserve, ReserveAdmin)
# Register your models here.
