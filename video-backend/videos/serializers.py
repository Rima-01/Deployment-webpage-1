#from rest_framework import serializers
#from .models import Video

#class VideoSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Video
#        fields = ['video_id', 'title', 'poster_url', 'video_url', 'click_count']
from rest_framework import serializers

class VideoSerializer(serializers.Serializer):
    video_id = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    poster_url = serializers.URLField()
    video_url = serializers.URLField()
    click_count = serializers.IntegerField()

    # Optional: Add custom validation logic if needed
    def validate_click_count(self, value):
        if value < 0:
            raise serializers.ValidationError("Click count cannot be negative.")
        return value
