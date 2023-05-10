import requests
import json


def create(request, messages):
    url = 'https://llm.asuperdomain.com/llama_async/'
    print("create: ", messages)
    post_response = requests.Session().post(url, data={
        'messages': json.dumps(messages)}, headers=dict(Referer=url))
    print(post_response.json())
    return post_response.json()
