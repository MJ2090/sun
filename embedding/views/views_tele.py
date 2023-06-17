from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot
from telegram.error import TelegramError
import asyncio


async def send_telegram_message(chat_id=6208450080, message="343434"):
    try:
        bot_token = "6186366547:AAHgkEeWAt_IkWJfxRvQGdRwB2P-ZIOprGY"
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message)
        return True
    except TelegramError as e:
        # Handle any errors that occur during sending the message
        print(f"Telegram Error: {str(e)}")
        return False
    
@csrf_exempt
def tele(request):
    my_json = json.loads(request.body)
    print("33333333333333333333300000000000000000000", my_json)
    print("333333333333333333333000000000000000000001", my_json['message'])
    print("33333333333333333333300000000000000000000", my_json['message']['chat'])
    print("33333333333333333333300000000000000000000", my_json['message']['chat']['id'])
    # chat_id = my_json['message'][0]['chat']['id']
    # print("33333333333333333333300000000000000000000", chat_id)
    # telegram_request = Request(
    #     request=request.body,
    #     headers=request.headers,
    #     input_stream=request,
    # )

    message = "You may have ADHD!"
    chat_id = my_json['message']['chat']['id']
    loop = asyncio.new_event_loop()
    task = loop.create_task(send_telegram_message(chat_id, message))
    loop.run_until_complete(task)

    # send_telegram_message(bot_token, chat_id, message)
    return HttpResponse(json.dumps({'question': 'okk'}))

# curl -F "url=https://www.asuperdomain.com/tele" -F "certificate=@a.pem" https://api.telegram.org/bot6186366547:AAHgkEeWAt_IkWJfxRvQGdRwB2P-ZIOprGY/getWebhookInfo