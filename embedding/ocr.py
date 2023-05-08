# import easyocr
import os


def read_image(file_name):
    result = "s"
    # reader = easyocr.Reader(['en'], gpu=False) # this needs to run only once to load the model into memory
    # result = reader.readtext(file_name)
    # for item in result:
    #     print(item[1])
    return result