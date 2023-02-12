from django.urls import path
from . import views

app_name='libraryseat'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('receive/', views.receive, name='receive'),
    path('status/', views.reserve_status, name='reserve_status'),
    path('admin/', views.seat_admin, name='seat_admin')
]

