from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.post_list, name='news'),
    path('edit/', views.post_new, name='post_new'),
    path('edit/<pk>/',views.post_edit, name='post_edit'),
    path('<pk>/',views.post_detail, name='post_detail'),
]
