from django.urls import path
from . import views

app_name='board'

urlpatterns = [
    path('create/<int:class_id>', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('detail/<int:assess_id>', views.detail, name='detail'),
    path('delete/<int:assess_id', views.delete, name='delete'),
]