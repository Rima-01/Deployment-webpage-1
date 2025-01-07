from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Watchlist
from .serializers import WatchlistSerializer
import boto3
from botocore.exceptions import ClientError

class WatchlistView(APIView):
#    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get(self, request):
        user_id = request.user.id
        watchlist = Watchlist.objects.filter(user_id=user_id)

        # Fetch video metadata from DynamoDB (using boto3)
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('VideosTable')
        enriched_watchlist = []
        for item in watchlist:
            try:
                response = table.get_item(Key={'video_id': item.video_id})
                if 'Item' in response:
                    video_data = response['Item']
                    video_data['timestamp'] = item.timestamp  # Add timestamp to metadata
                    enriched_watchlist.append(video_data)
            except ClientError as e:
                # Log the error and skip this video
                print(f"Error fetching video metadata: {e}")
                continue

        return Response({"watchlist": enriched_watchlist}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)  # Attach the current user ID
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, video_id):
        user_id = request.user.id
        deleted, _ = Watchlist.objects.filter(user_id=user_id, video_id=video_id).delete()
        if deleted:
            return Response({"message": "Video removed from watchlist."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Video not found in watchlist."}, status=status.HTTP_404_NOT_FOUND)
