from django.contrib import admin
from .models import ClassA, ClassA_Post

class ClassAAdmin(admin.ModelAdmin):
  pass
  list_display=('subject','professor','semester')
  # list_editable=('semester')
  list_filter=('subject','professor')
  # search_fields=('subject','professor','semester')

admin.site.register(ClassA, ClassAAdmin)
admin.site.register(ClassA_Post)
# Register your models here.
