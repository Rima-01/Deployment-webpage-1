from django.db import models

class Watchlist(models.Model):
    user_id = models.EmailField()  # User's email is used as the identifier
    video_id = models.CharField(max_length=255)  # Unique ID for the video
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when added

    def __str__(self):
        return f"User {self.user_id} - Video {self.video_id}"
