from django.contrib import admin
from .models import Reserve
# Register your models here.

class ReserveAdmin(admin.ModelAdmin):
  pass
  list_display=('room')
  search_fields=('author')

#  def room_number('room'):
 #   if room=='1':
  #    return 'B126'
   # else:
    #  return 'no'
  


admin.site.regiter(Reserve, ReserveAdmin)
