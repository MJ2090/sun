import requests
import json


def create(request, messages, prompt):
    url = 'https://llm.asuperdomain.com/glm_async/'
    print("create: ", messages)
    post_response = requests.Session().post(url, data={
        'messages': json.dumps(messages), 'prompt': prompt}, headers=dict(Referer=url))
    print("post_response: ", post_response.json())
    return post_response.json()
