from django.urls import path
from .views import WatchlistView

urlpatterns = [
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    path('watchlist/<str:video_id>/', WatchlistView.as_view(), name='watchlist-delete'),
]
