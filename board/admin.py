from django.contrib import admin
from .models import ClassA, ClassA_Post

class ClassAAdmin(admin.ModelAdmin):
  pass
  list_display=('subject','professor','semester','ox')
  search_fields=('subject','professor')
  ordering=('subject',)
  list_editable=('semester',)

  def ox(self, obj):
    if obj.professor=="이기범":
      return "o"
    return "x"

class ClassA_PostAdmin(admin.ModelAdmin):
  pass
  list_display=('subject','professor','semester','rate')

admin.site.register(ClassA, ClassAAdmin)
admin.site.register(ClassA_Post, ClassA_PostAdmin)
# Register your models here.
