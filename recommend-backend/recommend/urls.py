from django.urls import path
from . import views

urlpatterns = [
    path('recommendations/', views.recommendations_page, name='recommendations_page'),
    path('get_recommendations/', views.get_recommendations, name='get_recommendations'),
]
