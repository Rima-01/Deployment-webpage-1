#from django.urls import path
#from . import views

#urlpatterns = [
#    path('', views.posters_page, name='posters_page'),
#    path('list/', views.get_videos, name='get_videos'),
#    path('video/<str:video_id>/', views.get_video_url, name='get_video_url'),
#    path('video/<int:video_id>/', views.get_video_url, name='get_video_url'),
#    path('metadata/<str:video_id>/', views.get_video_metadata, name='get_video_metadata'),
#]

#from django.urls import path
#from . import views

#urlpatterns = [
#    path('', views.posters_page, name='posters_page'),
#    path('videos/', views.get_videos, name='get_videos'),
#    path('videos/play_video/<str:video_id>/', views.get_video_url, name='get_video_url'),
#]
#from django.urls import path
#from . import views

#urlpatterns = [
#    path('posters/', views.posters_page, name='posters_page'),  # Render posters.html
#    path('play_video/', views.video_page, name='video_page'),  # Render play_video.html
#    path('get_videos/', views.get_videos, name='get_videos'),  # Fetch videos for posters
#    path('videos/add_video/', views.add_video, name='add_video'),
#    path('play_video/<str:video_id>/', views.get_video_url, name='get_video_url'),  # Fetch video URL and increment click count
#]

from django.urls import path
from . import views

urlpatterns = [
    
    path('posters/', views.posters_page, name='posters_page'),  # Route to render the posters page
    path('play_video/', views.video_page, name='video_page'),  # Route to render the video playback page
    path('get_videos/', views.get_videos, name='get_videos'),  # API to fetch all videos with poster URLs
    path('play_video/<str:video_id>/', views.get_video_url, name='get_video_url'),  # API to fetch a specific video URL and increment click count
    path('add_video/', views.add_video, name='add_video'),  # API to add a new video if it doesn’t exist
]
