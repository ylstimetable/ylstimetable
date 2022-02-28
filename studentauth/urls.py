from django.urls import path
from . import views

app_name = 'studentauth'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/<int:user_id>', views.register, name='register')
]
