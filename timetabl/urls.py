from django.contrib import admin
from django.urls import path, include
from timetable import views

urlpatterns = [
    path('adminlee/', admin.site.urls),
    path('timetable/', include('timetable.urls')),
    path('common/', include('common.urls')),
    path('board/', include('board.urls')),
    path('', views.index, name='index'),
    path('freeboard/', include('freeboard.urls')),
]

handler404 = 'common.views.page_not_found'