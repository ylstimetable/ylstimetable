from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('result/', views.result, name='result'),
    path('search/', views.index, name='search'),
    path('addition/', views.addition, name='addition'),
    path('register/<int:class_id>', views.register, name='register'),
    path('delete/<int:class_id>', views.delete, name='delete'),
    path('address/<str:number>/<int:ban>', views.address, name='address'),
    path('manual/', views.manual_register, name='manual'),
    path('manual/delete/<int:class_id>', views.manual_delete, name='manual_delete'),
]
