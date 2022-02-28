from django.urls import path
from . import views

app_name='libraryseat'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('create/', views.create_receive, name='create_receive'),
    path('receive/', views.receive, name='receive'),
    path('random/', views.random, name='random'),
    path('register/', views.register, name='register')


]