#from rest_framework import serializers
#from .models import Video

#class VideoSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Video
#        fields = ['video_id', 'title', 'poster_url', 'video_url', 'click_count']
from rest_framework import serializers

class VideoSerializer(serializers.Serializer):
    video_id = serializers.CharField(max_length=255)  # Video ID (Primary Key)
    title = serializers.CharField(max_length=255)  # Title of the video
    description = serializers.CharField(max_length=500, allow_blank=True)  # Description (optional)
    poster_url = serializers.URLField()  # URL for the video poster
    video_url = serializers.URLField()  # URL for the video
    click_count = serializers.IntegerField(default=0) 