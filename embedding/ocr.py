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
import time
from embedding.ocr_bd import ocr_baidu


def recognize_image(file_name, source='xunfei'):
    request_time = time.time()
    result = "Nothing, no source found"
    if source=='tesseract':
        result = ocr_tesseract(file_name)
    if source=='xunfei':
        result = ocr_xunfei(file_name)
    if source=='baidu':
        result = ocr_baidu(file_name)
    return result, request_time


def ocr_tesseract(file_name):
    img = Image.open(file_name)
    text = pytesseract.image_to_string(img, lang="chi_sim")
    return text


def ocr_xunfei(file_name):
    APPId = "9153216a"  # 控制台获取
    APISecret = "NzY2ZTQzMjg4ZTE1ODgwN2Q0OGI2YzUx"  # 控制台获取
    APIKey = "8c236684482552b6f3dff60d6d8b4065"  # 控制台获取

    with open(file_name, "rb") as f:
        imageBytes = f.read()
    url = 'https://api.xf-yun.com/v1/private/sf8e6aca1'
    #url = 'https://cn-east-1.api.xf-yun.com/v1/ocr'

    body = {
        "header": {
            "app_id": APPId,
            "status": 3
        },
        "parameter": {
            "sf8e6aca1": {
                "category": "ch_en_public_cloud",
                "result": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            "sf8e6aca1_data_1": {
                "encoding": "jpg",
                "image": str(base64.b64encode(imageBytes), 'UTF-8'),
                "status": 3
            }
        }
    }

    request_url = assemble_ws_auth_url(url, "POST", APIKey, APISecret)

    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': APPId}
    # print(request_url)
    response = requests.post(request_url, data=json.dumps(body), headers=headers)
    # print(response)
    # print(response.content)

    # print("resp=>" + response.content.decode())
    tempResult = json.loads(response.content.decode())

    finalResult = base64.b64decode(tempResult['payload']['result']['text']).decode()
    finalResult = finalResult.replace(" ", "").replace("\n", "").replace("\t", "").strip()
    # print("text字段Base64解码后=>" + finalResult)
    finalResult_json = json.loads(finalResult)
    context = ""
    for page in finalResult_json['pages']:
        for line in page['lines']:
            print("line: ", line)
            if 'words' in line:
                tmp = ' '.join([word['content']for word in line['words'] if word['conf']>0.8])
                context += tmp + '\n'
    # print(context)
    return context

"""Private functions ..."""

class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema
        pass


def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        print("edidx <= 0")
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u


# build websocket auth request url
def assemble_ws_auth_url(requset_url, method="POST", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    print(date)
    # date = "Thu, 12 Dec 2019 01:57:27 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    print(signature_origin)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    print(authorization_origin)
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)
