from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

AWS_REGION = 'us-east-1'
S3_BUCKET = 'webpage-uploads-2'

# Render posters page
def posters_page(request):
    print("Template search paths:", settings.TEMPLATES[0]['DIRS']) 
    return render(request, 'posters.html')

# Render video page
def video_page(request):
    return render(request, 'play_video.html')

# Fetch videos and generate pre-signed URLs
def get_videos(request):
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table('VideosTable')
    s3 = boto3.client('s3', region_name=AWS_REGION)

    try:
        response = table.scan()
        items = response['Items']

        for item in items:
            # Generate pre-signed poster URL
            poster_key = item['poster_url'].split(f"{S3_BUCKET}/")[1]
            item['poster_url'] = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET, 'Key': poster_key},
                ExpiresIn=3600
            )

        return JsonResponse({'success': True, 'videos': items})
    except ClientError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Increment click count and return video pre-signed URL
@csrf_exempt
def get_video_url(request, video_id):
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table('VideosTable')
    s3 = boto3.client('s3', region_name=AWS_REGION)

    try:
        response = table.get_item(Key={'video_id': video_id})
        video = response['Item']

        # Generate pre-signed video URL
        video_key = video['video_url'].split(f"{S3_BUCKET}/")[1]
        video_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': video_key},
            ExpiresIn=3600
        )

        # Increment click count
        table.update_item(
            Key={'video_id': video_id},
            UpdateExpression="ADD click_count :increment",
            ExpressionAttributeValues={':increment': 1}
        )

        return JsonResponse({'success': True, 'video_url': video_url})
    except ClientError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
