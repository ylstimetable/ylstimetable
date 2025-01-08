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

admin.site.register(ClassD, ClassDAdmin)
admin.site.register(ClassM)
admin.site.register(Reserve, ReserveAdmin)
# Register your models here.
