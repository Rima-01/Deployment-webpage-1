#from django.contrib import admin
#from django.urls import path, include

#urlpatterns = [
    
#    path('videos/', include('videos.urls')),
#    path('', include('videos.urls')),
#]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('videos/', include('videos.urls')),  # Include routes from the videos app
]
