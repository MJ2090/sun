# import easyocr
import os
import requests

def read_image(file_name, source='osr_space'):
    if source=='osr_space':
        return ocr_space(file_name)
    return "Nothing"

def ocr_space(file_name):
    api_key = "K82589884488957"
    language = "eng"
    payload = {'isOverlayRequired': False,
               'apikey': api_key,
               'language': language,
               }
    with open(file_name, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={file_name: f},
                          data=payload,
                          )
    return r.content.decode()