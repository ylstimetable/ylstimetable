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
      return "B126"
    return "else"
 #   elif obj.room=="2":
  #    return "B127"
   # elif obj.room=="3":
#      return "B112"
 #   elif obj.room=="4":
  #    return "B113"
   # elif obj.room=="5":
#      return "B114"
 #   elif obj.room=="6":
  #    return "B116"
   # elif obj.room=="7":
#      return "212C"
 #   elif obj.room=="8":
  #    return "212D"
   # elif obj.room="9":
    #  return "212E"
#    return "212F"

admin.site.register(ClassD, ClassDAdmin)
admin.site.register(ClassM)
admin.site.register(Reserve, ReserveAdmin)
# Register your models here.
