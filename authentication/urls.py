#from django.urls import path
#from .views import signup_view, login_view

#urlpatterns = [
#    path('signup/', signup_view, name='signup'),
#    path('login/', login_view, name='login'),
#]
#from django.urls import path
#from rest_framework_simplejwt.views import (
#    TokenObtainPairView,
#    TokenRefreshView,
#)
from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]

