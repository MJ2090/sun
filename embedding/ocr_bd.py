# import easyocr
import os
import requests
from PIL import Image
import pytesseract
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json


def get_token():
    client_id='1BAfd9UCj2i0V8xw48A0iFK5'
    client_secret='nHjXXKImognC1HMG0FYBRVRxahFaqBPr'
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
    
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    res = json.loads(response.text)['access_token']
    print("sss: ", json.loads(response.text)['access_token'])
    return res


def ocr_baidu(file_name):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/doc_analysis"
    # 二进制方式打开图片文件
    f = open(file_name, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img,"language_type":"CHN_ENG","result_type":"big"}
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())
    res = ""
    for result in response.json()['results']:
        tmp = result['words']['word']
        res += tmp + '\n'

    return res