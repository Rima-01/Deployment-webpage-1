import requests
import boto3

AUTH_SERVICE_URL = "http://authentication_service/api/auth"
VIDEO_SERVICE_URL = "http://video_streaming_service/api/videos"

def get_user_details(token):
    response = requests.get(f"{AUTH_SERVICE_URL}/user/", headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    return response.json()

def get_video_details(video_id):
    response = requests.get(f"{VIDEO_SERVICE_URL}/{video_id}/")
    response.raise_for_status()
    return response.json()

def get_presigned_url(s3_key):
    s3 = boto3.client('s3')
    return s3.generate_presigned_url('get_object', Params={'Bucket': 'your_bucket', 'Key': s3_key}, ExpiresIn=3600)
