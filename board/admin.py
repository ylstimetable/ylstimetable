from django.contrib import admin
from .models import ClassA, ClassA_Post

class ClassAAdmin(admin.ModelAdmin):
  pass
  list_display = ('classname', 'professor')

admin.site.register(ClassA)
admin.site.register(ClassA_Post)
# Register your models here.
