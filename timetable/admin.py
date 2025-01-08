from django.contrib import admin
from .models import ClassD, ClassM
from studyroom.models import Reserve

class ClassDAdmin(admin.ModelAdmin):
  pass
  list_display=('title','professor','time','room')

class ReserveAdmin(admin.ModelAdmin):
  pass
  list_display=('room','room_name','date')
  def room_name(self, obj):
    if obj.room=="1":
      name="B126"
      return name
    elif obj.room=="2":
      name="B127"
      return name
    elif obj.room=="3":
      name="B112"
      return name
    elif obj.room=="4":
      name="B113"
      return name
    elif obj.room=="5":
      name="B114"
      return name
    elif obj.room=="6":
      name="B116"
      return name
    elif obj.room=="7":
      name="212C"
      return name
    elif obj.room=="8":
      name="212D"
      return name
    elif obj.room="9":
      name="212E"
      return name
    elif obj.room="10":
      name="212F"
      return name

admin.site.register(ClassD, ClassDAdmin)
admin.site.register(ClassM)
admin.site.register(Reserve, ReserveAdmin)
# Register your models here.
