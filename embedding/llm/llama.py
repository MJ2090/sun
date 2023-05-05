import requests
import json


def create(messages):
    url = 'https://llm.asuperdomain.com/test_async/'
    sess = requests.Session()
    csrf_token = None
    if csrf_token is None:
        get_response = sess.get(url)
        csrf_token = get_response.cookies['csrftoken']
    print("create: ", messages)
    post_response = sess.post(url, data={
                              'csrfmiddlewaretoken': csrf_token, 'messages': json.dumps(messages)}, headers=dict(Referer=url))
    print(post_response.json())
    return post_response.json()
