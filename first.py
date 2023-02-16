import torch
from transformers import pipeline

c = pipeline("sentiment-analysis")
res=c("I'm happy today")
print(res)
