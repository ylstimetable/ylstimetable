from django.contrib import admin
from django.urls import path, include
from timetable import views

urlpatterns = [
    path('adminlee/', admin.site.urls),
    path('timetable/', include('timetable.urls')),
    path('common/', include('common.urls')),
    path('board/', include('board.urls')),
    path('studyroom/', include('studyroom.urls')),
    path('', views.index, name='index'),
    path('freeboard/', include('freeboard.urls')),
    path('commonboard/', include('commonboard.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('studentauth.urls')),
    path('libraryseat/', include('libraryseat.urls')),
    path('survey/', include('survey.urls')),
    path('inquiry/', include('inquiry.urls'))
]

admin.site.index_title = "YLS TimeTable"
admin.site.site_header = "YLS TimeTable Admin"

handler404 = 'common.views.page_not_found'
