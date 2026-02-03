from django.urls import path
from . import views


urlpatterns = [
    path('', views.story_list, name='stories'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail')
]
