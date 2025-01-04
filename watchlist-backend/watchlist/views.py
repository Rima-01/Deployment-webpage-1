import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Watchlist
from .serializers import WatchlistSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

# AWS DynamoDB and S3 setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Replace 'your-region'
VIDEOS_TABLE_NAME = 'VideosTable'
videos_table = dynamodb.Table(VIDEOS_TABLE_NAME)

s3_client = boto3.client('s3', region_name='us-east-1')  # Replace 'your-region'
S3_BUCKET_NAME = 'webpage-uploads-2'  # Replace 'your-bucket-name'

@method_decorator(csrf_exempt, name='dispatch')
class WatchlistView(APIView):
    def get(self, request):
        """
        Fetch the user's watchlist and enrich it with video metadata from DynamoDB.
        """
        user_id = request.GET.get('user_id')

        if not user_id:
            logger.warning("GET request without user_id.")
            return Response({"error": "User ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user's watchlist from PostgreSQL
        watchlist = Watchlist.objects.filter(user_id=user_id.lower())  # Ensure case-insensitivity

        if not watchlist.exists():
            logger.info(f"Watchlist is empty for user_id: {user_id}")
            return Response({"message": "Your watchlist is empty."}, status=status.HTTP_200_OK)

        enriched_videos = []
        for item in watchlist:
            video_id = item.video_id
            try:
                # Fetch video metadata from DynamoDB
                response = videos_table.get_item(Key={'video_id': video_id})
                video_metadata = response.get('Item', {})
                if video_metadata:
                    # Generate a pre-signed URL for the poster
                    poster_key = video_metadata.get('poster_url')
                    presigned_url = s3_client.generate_presigned_url(
                        'get_object',
                        Params={'Bucket': S3_BUCKET_NAME, 'Key': poster_key},
                        ExpiresIn=3600  # URL expires in 1 hour
                    )
                    enriched_videos.append({
                        'video_id': video_id,
                        'title': video_metadata.get('title'),
                        'poster_url': presigned_url,
                    })
            except Exception as e:
                logger.error(f"Error fetching metadata for video_id {video_id}: {e}")
                continue

        logger.info(f"Retrieved watchlist for user_id: {user_id}")
        return Response(enriched_videos, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Add a video to the user's watchlist after checking for duplicates.
        """
        user_id = request.data.get('user_id')

        if not user_id:
            logger.warning("POST request without user_id.")
            return Response({"error": "User ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        video_id = request.data.get('video_id')
        if not video_id:
            logger.warning("POST request without video_id.")
            return Response({"error": "Video ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if video is already in the watchlist
        if Watchlist.objects.filter(user_id=user_id.lower(), video_id=video_id).exists():
            logger.info(f"Duplicate video_id {video_id} for user_id {user_id}.")
            return Response({"message": "Video already exists in your watchlist."}, status=status.HTTP_409_CONFLICT)

        # Serialize and save the new entry
        data = {'user_id': user_id.lower(), 'video_id': video_id}
        serializer = WatchlistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Video {video_id} added to watchlist for user_id {user_id}.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, video_id):
        """
        Remove a video from the user's watchlist.
        """
        user_id = request.GET.get('user_id')

        if not user_id:
            logger.warning("DELETE request without user_id.")
            return Response({"error": "User ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        if not video_id:
            logger.warning("DELETE request without video_id.")
            return Response({"error": "Video ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the entry from the database
        deleted_count, _ = Watchlist.objects.filter(user_id=user_id.lower(), video_id=video_id).delete()

        if deleted_count == 0:
            logger.warning(f"Video {video_id} not found in watchlist for user_id {user_id}.")
            return Response({"error": "Video not found in watchlist."}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"Video {video_id} removed from watchlist for user_id {user_id}.")
        return Response({"message": "Video removed from watchlist."}, status=status.HTTP_204_NO_CONTENT)
