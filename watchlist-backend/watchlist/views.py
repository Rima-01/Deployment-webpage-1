import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Watchlist
from .serializers import WatchlistSerializer

# Initialize DynamoDB and S3
dynamodb = boto3.resource('dynamodb', region_name='your-region')  # Replace 'your-region'
VIDEOS_TABLE_NAME = 'VideosTable'
videos_table = dynamodb.Table(VIDEOS_TABLE_NAME)

s3_client = boto3.client('s3', region_name='your-region')  # Replace with your AWS region
S3_BUCKET_NAME = 'your-bucket-name'  # Replace with your S3 bucket name

class WatchlistView(APIView):
    def get(self, request):
        """
        Fetch the user's watchlist, handle empty table, enrich it with video metadata, 
        and generate pre-signed URLs for poster images.
        """
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.user.email  # Assuming email is used as the user ID

        # Fetch user's watchlist from PostgreSQL
        watchlist = Watchlist.objects.filter(user_id=user_id)

        if not watchlist.exists():
            return Response({"message": "Your watchlist is empty."}, status=status.HTTP_200_OK)

        # Fetch video metadata from DynamoDB and generate pre-signed URLs
        enriched_videos = []
        for item in watchlist:
            video_id = item.video_id
            try:
                # Query DynamoDB for the video metadata
                response = videos_table.get_item(Key={'video_id': video_id})
                video_metadata = response.get('Item', {})
                if video_metadata:
                    # Generate a pre-signed URL for the poster
                    poster_key = video_metadata.get('poster_url')  # Poster S3 key
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
                print(f"Error fetching metadata for video_id {video_id}: {e}")
                continue

        return Response(enriched_videos, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Add a video to the user's watchlist after checking for existing data.
        """
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.user.email  # Assuming email is used as the user ID
        data = request.data
        data['user_id'] = user_id

        # Check if the video already exists in the user's watchlist
        video_id = data.get('video_id')
        if Watchlist.objects.filter(user_id=user_id, video_id=video_id).exists():
            return Response({"message": "Video already exists in your watchlist."}, status=status.HTTP_409_CONFLICT)

        # Add the video to the watchlist
        serializer = WatchlistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, video_id):
        """
        Remove a video from the user's watchlist.
        """
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.user.email
        deleted_count, _ = Watchlist.objects.filter(user_id=user_id, video_id=video_id).delete()

        if deleted_count == 0:
            return Response({"error": "Video not found in watchlist."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Video removed from watchlist."}, status=status.HTTP_204_NO_CONTENT)
