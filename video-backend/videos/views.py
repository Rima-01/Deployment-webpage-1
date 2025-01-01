from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .serializers import VideoSerializer
import boto3
from botocore.exceptions import ClientError
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

AWS_REGION = 'us-east-1'
S3_BUCKET = 'webpage-uploads-2'

# Render posters page
def posters_page(request):
    return render(request, 'posters.html')

# Render video playback page
def video_page(request):
    return render(request, 'play_video.html')

# Check if table is empty and populate with default data
def check_and_populate_table():
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table('VideosTable')

    try:
        response = table.scan()
        if 'Items' not in response or len(response['Items']) == 0:
            logger.info("DynamoDB table is empty. Populating with default values.")
            default_data = [
                {
                    "video_id": "1",
                    "title": "Sample Video 1",
                    "description": "Description for video 1",
                    "poster_url": f"https://{S3_BUCKET}.s3.amazonaws.com/posters/poster1.jpg",
                    "video_url": f"https://{S3_BUCKET}.s3.amazonaws.com/videos/video1.mp4",
                    "click_count": 0
                },
                {
                    "video_id": "2",
                    "title": "Sample Video 2",
                    "description": "Description for video 2",
                    "poster_url": f"https://{S3_BUCKET}.s3.amazonaws.com/posters/poster2.jpg",
                    "video_url": f"https://{S3_BUCKET}.s3.amazonaws.com/videos/video2.mp4",
                    "click_count": 0
                }
            ]
            for item in default_data:
                table.put_item(Item=item)
            logger.info("Default data added to the DynamoDB table.")
    except ClientError as e:
        logger.error(f"Error populating DynamoDB table: {e}")

# Fetch all video posters and pre-signed URLs
def get_videos(request):
    check_and_populate_table()  # Ensure the table has data
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table('VideosTable')
    s3 = boto3.client('s3', region_name=AWS_REGION)

    try:
        response = table.scan()
        if 'Items' not in response or len(response['Items']) == 0:
            return JsonResponse({'success': False, 'error': 'No videos found.'}, status=404)

        items = response['Items']
        for item in items:
            # Generate pre-signed poster URL
            poster_key = item['poster_url'].split(f"{S3_BUCKET}/")[1]
            item['poster_url'] = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET, 'Key': poster_key},
                ExpiresIn=3600
            )

        # Validate and serialize the data
        serializer = VideoSerializer(data=items, many=True)
        if serializer.is_valid():
            return JsonResponse({'success': True, 'videos': serializer.data})
        else:
            return JsonResponse({'success': False, 'error': serializer.errors}, status=400)
    except ClientError as e:
        logger.error(f"Error fetching videos: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Add video if it doesn't exist
@csrf_exempt
def add_video(request):
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        table = dynamodb.Table('VideosTable')

        try:
            # Parse incoming data
            data = json.loads(request.body)

            # Validate data with the serializer
            serializer = VideoSerializer(data=data)
            if not serializer.is_valid():
                return JsonResponse({'success': False, 'error': serializer.errors}, status=400)

            video_id = data.get('video_id')

            # Check if the video already exists
            response = table.get_item(Key={'video_id': video_id})
            if 'Item' in response:
                return JsonResponse({'success': False, 'error': 'Video already exists'}, status=400)

            # Add the new video to the DynamoDB table
            table.put_item(Item=data)
            logger.info(f"Video {video_id} added successfully.")
            return JsonResponse({'success': True, 'message': 'Video added successfully'})
        except ClientError as e:
            logger.error(f"DynamoDB ClientError: {e}")
            return JsonResponse({'success': False, 'error': 'DynamoDB error: ' + str(e)}, status=500)
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload received.")
            return JsonResponse({'success': False, 'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({'success': False, 'error': 'Unexpected error: ' + str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

# Fetch video URL and increment click count
@csrf_exempt
def get_video_url(request, video_id):
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table('VideosTable')
    s3 = boto3.client('s3', region_name=AWS_REGION)

    try:
        # Fetch video details from DynamoDB
        response = table.get_item(Key={'video_id': video_id})
        video = response.get('Item', {})

        if not video:
            return JsonResponse({'success': False, 'error': 'Video not found'}, status=404)

        # Generate pre-signed video URL
        video_key = video['video_url'].split(f"{S3_BUCKET}/")[1]
        video_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': video_key},
            ExpiresIn=3600  # URL valid for 1 hour
        )

        # Increment the click count
        table.update_item(
            Key={'video_id': video_id},
            UpdateExpression="ADD click_count :increment",
            ExpressionAttributeValues={':increment': 1}
        )

        logger.info(f"Video {video_id} accessed successfully.")
        return JsonResponse({'success': True, 'video_url': video_url})
    except ClientError as e:
        logger.error(f"DynamoDB ClientError: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'success': False, 'error': 'Unexpected error occurred.'}, status=500)
