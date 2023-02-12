from django.urls import path
from . import views

app_name='survey'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('detail/<int:post_id>', views.detail, name='detail')
    #path('post/comment/create/<int:post_id>', views.comment_create, name='comment_create')
]

