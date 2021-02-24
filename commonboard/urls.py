from django.urls import path
from . import views

app_name='commonboard'

urlpatterns = [
    path('post/create/', views.announce_create, name='create'),
    path('list/', views.list, name='list'),
    path('detail/<int:announce_id>', views.detail, name='detail'),
    path('post/delete/<int:announce_id>', views.announce_delete, name='delete'),

]