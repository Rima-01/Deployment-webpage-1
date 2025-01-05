from django.urls import path
from .views import WatchlistView
#from django.shortcuts import redirect

#def redirect_to_watchlist(request):
#    return redirect('/watchlist/')

urlpatterns = [
#    path('', redirect_to_watchlist),  # Redirect root URL to /watchlist/
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),  # Handles /api/watchlist/
#    path('watchlist/',WatchlistView, name='watchlist'),  # Handles /api/watchlist/
    path('watchlist/<str:video_id>/', WatchlistView.as_view(), name='watchlist-detail'),  # Handles /api/watchlist/<video_id>/
#    path('watchlist/<str:video_id>/', WatchlistView, name='watchlist-detail'),  # Handles /api/watchlist/<video_id>/
    path('watchlist/<str:user_id>/', WatchlistView.as_view(), name='watchlist'),
]
