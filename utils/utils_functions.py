import random

import requests
from django.conf import settings


def is_verified(f):
    def inner(request, *args, **kwargs):
        if not request.auth.is_verified:
            return 403, {'msg': 'You are not verified yet, please verify your account'}
        return f(request, *args, **kwargs)

    return inner


def generate_random_otp():
    return random.randint(1000, 9999)


# Upload image in each model admin
def upload_image(obj, image_file):
    if image_file:
        res = requests.post(
            url=settings.IMGBB_URL,
            files={'image': image_file.read()},
            params={'key': settings.IMGBB_KEY}
        )
        if res.ok:
            obj.image = res.json()['data']['url']
            obj.thumbnail = res.json()['data']['thumb']['url']
        else:
            obj.image = None
    return obj
