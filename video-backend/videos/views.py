from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import boto3
from botocore.exceptions import ClientError

# AWS Configuration
AWS_REGION = 'us-east-1'  # Replace with your region
S3_BUCKET = 'webpage-uploads-1'  # Replace with your bucket name

# View to render the posters page (HTML template)
def posters_page(request):
    return render(request, 'posters.html')

# Fetch the list of videos (posters and metadata) from DynamoDB with presigned poster URLs
def get_videos(request):
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table('VideosTable')
    s3 = boto3.client('s3', region_name=AWS_REGION)

    try:
        # Fetch items from DynamoDB
        response = table.scan()
        items = response['Items']

        # Generate pre-signed URLs for poster images
        for item in items:
            poster_url = item.get('poster_url')
            if poster_url:
                # Extract the S3 key from the URL
                key = poster_url.split(f"{S3_BUCKET}/")[1]
                presigned_poster_url = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': S3_BUCKET, 'Key': key},
                    ExpiresIn=3600  # URL valid for 1 hour
                )
                item['poster_url'] = presigned_poster_url

        return JsonResponse({'success': True, 'videos': items}, safe=False)
    except ClientError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Increment the click count for a video and return the video pre-signed URL
@csrf_exempt
def get_video_url(request, video_id):
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        table = dynamodb.Table('VideosTable')
        s3 = boto3.client('s3', region_name=AWS_REGION)

        try:
            # Fetch the video item
            response = table.get_item(Key={'video_id': video_id})
            if 'Item' not in response:
                return JsonResponse({'success': False, 'error': 'Video not found'}, status=404)

            video_item = response['Item']

            # Increment the click count atomically
            table.update_item(
                Key={'video_id': video_id},
                UpdateExpression='ADD click_count :increment',
                ExpressionAttributeValues={':increment': 1},
                ReturnValues='UPDATED_NEW'
            )

            # Generate pre-signed URL for the video
            video_url = video_item.get('video_url')
            if video_url:
                key = video_url.split(f"{S3_BUCKET}/")[1]
                presigned_video_url = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': S3_BUCKET, 'Key': key},
                    ExpiresIn=3600  # URL valid for 1 hour
                )
                return JsonResponse({'success': True, 'video_url': presigned_video_url})
            else:
                return JsonResponse({'success': False, 'error': 'Video URL not found'}, status=404)
        except ClientError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
