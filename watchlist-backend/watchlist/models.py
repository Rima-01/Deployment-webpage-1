from django.db import models

class Watchlist(models.Model):
    user_id = models.EmailField()  # Assuming email is used as the user ID
    video_id = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id} - Video {self.video_id}"
