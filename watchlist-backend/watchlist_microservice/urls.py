"""
URL configuration for watchlist_microservice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import HttpResponse  # Import this at the top
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib import admin  # Import the admin module
def root_view(request):
    return HttpResponse("Welcome to the Watchlist API!", status=200)

urlpatterns = [
    path('', root_view, name='root'),  # Handle the root URL
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Default login view
#    path('logout/watchlist/', auth_views.LogoutView.as_view(), name='logout'),  # Default logout view
    path('api/', include('watchlist.urls')),  # Watchlist app routes
]
