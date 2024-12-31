#from django.contrib import admin
#from .models import Video

#@admin.register(Video)
#class VideoAdmin(admin.ModelAdmin):
#    list_display = ('video_id', 'title', 'click_count')
from django.shortcuts import render
import boto3

def custom_admin_dashboard(request):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VideosTable')
    response = table.scan()
    items = response.get('Items', [])
    return render(request, 'admin.html', {'videos': items})
