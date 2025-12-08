from django.shortcuts import render
from django.http import HttpResponse

import requests

import json
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from django.views.decorators.clickjacking import xframe_options_exempt

BASE_DIR = Path(__file__).resolve().parent.parent

with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))

def index(request):
    return HttpResponse("Hello world!")

@xframe_options_exempt
def bloggerApiGetLatestPost(request):
    try:
        blogger_apiv3 = get_secret('blogger_apiv3')
        mapbox_api = get_secret('mapbox_api')
        headers = {"Referer": "https://api.roadtripsandhikes.org"}
        response = requests.get("https://www.googleapis.com/blogger/v3/blogs/5929721860344397604/posts?",
            params = {
                'key': blogger_apiv3,
                'labels': '^ Hikes',
                'fetchBodies': 'true',
                'fetchImages': 'true',
                'maxResults': 1,
                'orderBy': 'PUBLISHED',
            },
            headers=headers,
            timeout=10  # Add timeout to prevent hanging
        )
        response.raise_for_status()  # Raise exception for bad status codes
        
        post_info_json = response.json().pop('items')
        post_published = post_info_json[0]['published']
        # post_label = post_info_json[0]['labels']
        post_url = post_info_json[0]['url']
        post_title = post_info_json[0]['title']
        post_image_url = post_info_json[0]['images'][0]['url']
        try:
            post_location = post_info_json[0]['location']
            post_info = {'latest_post': {'published': post_published, 'post_url': post_url, 'title': post_title, 'image_url': post_image_url,'post_location': post_location,'mba': mapbox_api }}
        except KeyError:
            post_info = {'latest_post': {'published': post_published, 'post_url': post_url, 'title': post_title, 'image_url': post_image_url,'mba': mapbox_api }}
        # post_info = {'latest_post': {'published': post_published, 'post_label': post_label, 'post_url': post_url, 'title': post_title, 'image_url': post_image_url,'post_location': post_location,'mba': mapbox_api }}
        post_info_sanitized = json.dumps(post_info, indent = 4)

        return HttpResponse(post_info_sanitized, content_type='application/json')
    except Exception as e:
        # Return error with proper CORS headers
        error_response = json.dumps({'error': 'Service temporarily unavailable', 'detail': str(e)})
        response = HttpResponse(error_response, content_type='application/json', status=503)
        response['Access-Control-Allow-Origin'] = 'https://www.roadtripsandhikes.org'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
