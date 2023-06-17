from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot
from telegram.error import TelegramError


def send_telegram_message(bot_token, chat_id, message):
    try:
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=message)
        return True
    except TelegramError as e:
        # Handle any errors that occur during sending the message
        print(f"Telegram Error: {str(e)}")
        return False
    
@csrf_exempt
def tele(request):
    print("33333333333333333333300000000000000000000", request.body)
    # telegram_request = Request(
    #     request=request.body,
    #     headers=request.headers,
    #     input_stream=request,
    # )

    bot_token = "6186366547:AAHgkEeWAt_IkWJfxRvQGdRwB2P-ZIOprGY"
    message = "Hello, Telegram!"
    chat_id = 6208450080

    send_telegram_message(bot_token, chat_id, message)
    return HttpResponse(json.dumps({'question': 'okk'}))

# curl -F "url=https://www.asuperdomain.com/tele" -F "certificate=@a.pem" https://api.telegram.org/bot6186366547:AAHgkEeWAt_IkWJfxRvQGdRwB2P-ZIOprGY/getWebhookInfo