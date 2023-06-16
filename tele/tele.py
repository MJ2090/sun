import requests

url2 = 'https://api.telegram.org:443/bot6186366547:AAHgkEeWAt_IkWJfxRvQGdRwB2P-ZIOprGY/setWebhook?url=https://asuperdomain.com/tele'
url1 = 'https://api.telegram.org/bot6186366547:AAHgkEeWAt_IkWJfxRvQGdRwB2P-ZIOprGY/getUpdates'
url = 'https://api.telegram.org/bot6186366547:AAHgkEeWAt_IkWJfxRvQGdRwB2P-ZIOprGY/getMe'
myobj = {'somekey': 'somevalue'}

x = requests.post(url, json = myobj)

print(x.text)