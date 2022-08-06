from django.urls import path
from . import views

app_name='libraryseat'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('create/', views.create_receive, name='create_receive'),
    path('receive/', views.receive, name='receive'),
    path('random/', views.random, name='random'),
    path('register/', views.register, name='register'),
    path('status/', views.reserve_status, name='reserve_status'),
    path('register_seat/<int:seat_number>/', views.seat_register, name='seat_register'),
    path('admin/', views.seat_admin, name='seat_admin'),
    path('floor/', views.floor, name='floor')


]