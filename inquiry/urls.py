from django.urls import path
from . import views

app_name='inquiry'

urlpatterns = [
    path('write/', views.write, name='write'),
    path('receive/', views.receive, name='receive')
]
