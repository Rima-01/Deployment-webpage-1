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

# Fetch all video posters and pre-signed URLs
def get_videos(request):
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
            if 'poster_url' in item and f"{S3_BUCKET}/" in item['poster_url']:
                poster_key = item['poster_url'].split(f"{S3_BUCKET}/")[1]
                item['poster_url'] = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': S3_BUCKET, 'Key': poster_key},
                    ExpiresIn=3600
                )
            else:
                logger.warning(f"Invalid or missing poster_url for video_id: {item.get('video_id')}")
                item['poster_url'] = None  # Handle missing or invalid URLs gracefully

        return JsonResponse({'success': True, 'videos': items})
    except ClientError as e:
        logger.error(f"Error fetching videos: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'success': False, 'error': 'Unexpected error occurred.'}, status=500)

# Add video if it doesn't exist or if the table is empty
@csrf_exempt
def add_video(request):
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        table = dynamodb.Table('VideosTable')

        try:
            # Parse incoming data
            data = json.loads(request.body)
            video_id = data.get('video_id')

            # Validate data with the serializer
            serializer = VideoSerializer(data=data)
            if not serializer.is_valid():
                return JsonResponse({'success': False, 'error': serializer.errors}, status=400)

            # Check if the table is empty or the video does not exist
            response = table.scan()
            if 'Items' not in response or len(response['Items']) == 0:
                # Table is empty, add the video
                table.put_item(Item=data)
                logger.info("Table was empty. Added first video entry.")
                return JsonResponse({'success': True, 'message': 'Video added successfully as the first entry.'})
            else:
                # Table is not empty; check if video_id already exists
                existing_video = table.get_item(Key={'video_id': video_id})
                if 'Item' in existing_video:
                    logger.info(f"Video {video_id} already exists in the table.")
                    return JsonResponse({'success': False, 'error': 'Video already exists.'})
                
                # Video does not exist; add it to the table
                table.put_item(Item=data)
                logger.info(f"Video {video_id} added to the table.")
                return JsonResponse({'success': True, 'message': 'Video added successfully.'})
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
        if 'video_url' in video and f"{S3_BUCKET}/" in video['video_url']:
            video_key = video['video_url'].split(f"{S3_BUCKET}/")[1]
            video_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET, 'Key': video_key},
                ExpiresIn=3600  # URL valid for 1 hour
            )
        else:
            logger.warning(f"Invalid or missing video_url for video_id: {video_id}")
            return JsonResponse({'success': False, 'error': 'Invalid video URL'}, status=400)

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
