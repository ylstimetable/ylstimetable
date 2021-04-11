from django.urls import path
from . import views

app_name='board'

urlpatterns = [
    path('create/<int:classa_id>', views.create, name='create'),
    path('createtool/<int:classa_id>', views.create_tool, name='create_tool'),
    path('list/', views.list, name='list'),
    path('detail/<int:classa_id>', views.detail, name='detail'),
    path('result/', views.result, name='result'),

]