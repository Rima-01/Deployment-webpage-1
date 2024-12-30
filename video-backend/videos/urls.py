from django.urls import path
from . import views

urlpatterns = [
    path('', views.posters_page, name='posters_page'),
    path('list/', views.get_videos, name='get_videos'),
    path('video/<str:video_id>/', views.get_video_url, name='get_video_url'),
    path('metadata/<str:video_id>/', views.get_video_metadata, name='get_video_metadata'),
]
