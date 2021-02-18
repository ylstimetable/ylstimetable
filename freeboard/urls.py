from django.urls import path
from . import views

app_name='freeboard'

urlpatterns = [
    path('post/create/', views.post_create, name='create'),
    path('list/', views.list, name='list'),
    path('detail/<int:post_id>', views.detail, name='detail'),
    path('post/delete/<int:post_id>', views.post_delete, name='delete'),
    path('post/comment/create/<int:post_id>', views.comment_create, name='comment_create'),
    path('post/comment/modify/<int:comment_id>', views.comment_modify, name='comment_modify'),
    path('post/comment/delete/<int:comment_id>', views.comment_delete, name='comment_delete'),

]