from django.urls import path
from . import views

app_name='libraryseat'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('detail/<int:post_id>', views.detail, name='detail'),
    path('post/comment/create/<int:post_id>', views.comment_create, name='comment_create'),
    path('admin/', views.seat_admin, name='seat_admin')
]

