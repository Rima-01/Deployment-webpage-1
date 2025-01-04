from django.urls import path
from .views import WatchlistView

urlpatterns = [
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),  # Handles /api/watchlist/
#    path('',WatchlistView, name='watchlist'),  # Handles /api/watchlist/
    path('watchlist/<str:video_id>/', WatchlistView.as_view(), name='watchlist-detail'),  # Handles /api/watchlist/<video_id>/
#    path('<str:video_id>/', WatchlistView, name='watchlist-detail'),  # Handles /api/watchlist/<video_id>/

]
