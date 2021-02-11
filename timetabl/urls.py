from django.contrib import admin
from django.urls import path, include
from timetable import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('timetable/', include('timetable.urls')),
    path('common/', include('common.urls')),
    path('board/', include('board.urls')),
    path('', views.index, name='index'),
]


handler404 = 'common.views.page_not_found'