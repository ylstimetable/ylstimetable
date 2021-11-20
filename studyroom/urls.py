from django.urls import path
from . import views

app_name = 'studyroom'

urlpatterns = [
    path('<int:room_num>/', views.index, name='index'),
    path('register/', views.register, name='register'),
]
