from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# View to render the posters page (HTML template)
def posters_page(request):
    return render(request, 'posters.html')

# Fetch the list of videos (posters and metadata) from DynamoDB
def get_videos(request):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VideosTable')
    try:
        response = table.scan()
        items = response['Items']
        return JsonResponse({'success': True, 'videos': items}, safe=False)
    except ClientError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Increment the click count for a video and return the video URL
@csrf_exempt
def get_video_url(request, video_id):
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('VideosTable')
        try:
            # Increment the click count atomically
            update_response = table.update_item(
                Key={'video_id': video_id},
                UpdateExpression='ADD click_count :increment',
                ExpressionAttributeValues={':increment': 1},
                ReturnValues='UPDATED_NEW'
            )
            updated_count = update_response['Attributes']['click_count']

            # Fetch the video URL from the item
            get_response = table.get_item(Key={'video_id': video_id})
            if 'Item' not in get_response:
                return JsonResponse({'success': False, 'error': 'Video not found'}, status=404)

            video_item = get_response['Item']
            video_url = video_item['video_url']

            # Generate presigned URL for the video from S3
            s3 = boto3.client('s3')
            s3_components = video_url.replace("https://", "").split("/", 1)
            bucket_name = s3_components[0]
            key = s3_components[1]
            presigned_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': key},
                ExpiresIn=3600  # URL expires in 1 hour
            )

            return JsonResponse({'success': True, 'video_url': presigned_url, 'updated_click_count': updated_count})
        except NoCredentialsError:
            return JsonResponse({'success': False, 'error': 'AWS credentials not configured'}, status=500)
        except ClientError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# API to fetch video metadata for a specific video
def get_video_metadata(request, video_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VideosTable')
    try:
        response = table.get_item(Key={'video_id': video_id})
        if 'Item' in response:
            return JsonResponse({'success': True, 'video': response['Item']})
        else:
            return JsonResponse({'success': False, 'error': 'Video not found'}, status=404)
    except ClientError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
