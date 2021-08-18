from django.shortcuts import render
from django.http import HttpResponse

import requests

import json
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

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

def bloggerApiGetLatestPost(request):
    blogger_apiv3 = get_secret('blogger_apiv3')
    headers = {"Referer": "https://api.roadtripsandhikes.org"}
    response = requests.get("https://www.googleapis.com/blogger/v3/blogs/5929721860344397604/posts?",
        params = {
            'key': blogger_apiv3,
            'fetchBodies': 'true',
            'fetchImages': 'true',
            'maxResults': 1,
            'orderBy': 'PUBLISHED',
        },
        headers=headers
    )
    post_info_json = response.json().pop('items')
    post_published = post_info_json[0]['published']
    post_url = post_info_json[0]['url']
    post_title = post_info_json[0]['title']
    post_image_url = post_info_json[0]['images'][0]['url']
    post_info = {'latest_post': {'published': post_published, 'post_url': post_url, 'title': post_title, 'image_url': post_image_url }}
    post_info_sanitized = json.dumps(post_info, indent = 4)
    return HttpResponse(post_info_sanitized, content_type='application/json')
