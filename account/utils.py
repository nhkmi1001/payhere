import random
from .models import Url
from django.conf import settings
from django.http import HttpResponseRedirect

def convert():
    encoding = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                'l', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3',
                '4', '5', '6', '7', '8' ,'9',
                ]
    while True:
        new_url = ''.join(random.sample(encoding,8))
        try:
           url = Url.objects.get(link=new_url)
        except:
            return new_url

def original(request, new_url):
    new_link = settings.SITE_URL + new_url
    url = Url.objects.get(short_link=new_link)
    return HttpResponseRedirect(url.link)
     