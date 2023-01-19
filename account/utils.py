from django.conf import settings
import base64
from datetime import datetime
from ast import literal_eval

def make_dict_to_url(data:dict) -> str:
    url = base64.urlsafe_b64encode(bytes(str(data), 'UTF-8')).decode("UTF-8").rstrip("=")
    return url

def make_url_to_dict(url:str) -> dict:
    pad = "=" * (4 - (len(url) % 4))
    url = url + pad
    try: # 옳바르지 않은 url입력을 대비
        str_dict = base64.urlsafe_b64decode(bytes(url, 'UTF-8')).decode("UTF-8") 
    except: # 특정 Error를 raise하지 않는다
        return False
    data_dict = literal_eval(str_dict)
    return data_dict

def check_valid_log_url(url:str) -> bool:
    log_dict = make_url_to_dict(url)
    if not log_dict:
        return False
    expiration_time = log_dict.get('expiration_time', '')
    is_valid_time = datetime.now().strftime('%y-%m-%d %H:%M:%S') <= str(expiration_time)
    if is_valid_time:
        return True
    return False