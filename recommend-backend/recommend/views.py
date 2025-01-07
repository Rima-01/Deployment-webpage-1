from django.http import JsonResponse
from django.shortcuts import render
import boto3
from botocore.exceptions import ClientError
import logging

# Configure logging
logger = logging.getLogger(__name__)

AWS_REGION = 'us-east-1'
S3_BUCKET = 'webpage-uploads-2'

# Fetch top 3 videos based on click count
def get_recommendations(request):
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table('VideosTable')
    s3 = boto3.client('s3', region_name=AWS_REGION)

    try:
        # Scan the DynamoDB table
        response = table.scan()
        if 'Items' not in response or len(response['Items']) == 0:
            return JsonResponse({'success': False, 'error': 'No videos found.'}, status=404)

        # Sort videos by click_count in descending order
        videos = sorted(response['Items'], key=lambda x: int(x['click_count']), reverse=True)
        top_videos = videos[:3]  # Get the top 3 videos

        # Generate pre-signed URLs for posters
        for video in top_videos:
            if 'poster_url' in video and "amazonaws.com/" in video['poster_url']:
                poster_key = video['poster_url'].split("amazonaws.com/")[1]
                video['poster_url'] = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': S3_BUCKET, 'Key': poster_key},
                    ExpiresIn=3600  # URL valid for 1 hour
                )
            else:
                logger.warning(f"Invalid or missing poster_url for video_id: {video.get('video_id')}")
                video['poster_url'] = None  # Handle missing poster_url gracefully

        return JsonResponse({'success': True, 'videos': top_videos})
    except ClientError as e:
        logger.error(f"Error fetching recommendations: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'success': False, 'error': 'Unexpected error occurred.'}, status=500)

# Render the recommendation page
def recommendations_page(request):
    return render(request, 'recommendations.html')
