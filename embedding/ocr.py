import easyocr
import os

reader = easyocr.Reader(['ch_sim','en'], gpu=False) # this needs to run only once to load the model into memory
result = reader.readtext('/Users/minjunzhu/Desktop/dddddd.png')
print(result)