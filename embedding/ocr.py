# import easyocr
import os
import requests
from PIL import Image
import pytesseract

def read_image(file_name, source='tesseract'):
    if source=='osr_space':
        return ocr_space(file_name)
    if source=='tesseract':
        return ocr_tesseract(file_name)
    return "Nothing, no source found"


def ocr_tesseract(file_name):
    img = Image.open(file_name)
    text = pytesseract.image_to_string(img)
    return text


def ocr_space(file_name):
    api_key = "K82589884488957"
    language = "chs"
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
