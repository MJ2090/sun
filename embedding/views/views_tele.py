from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot
from telegram.error import TelegramError
import asyncio
from embedding.openai.features import feature_chat


async def send_telegram_message(chat_id=6208450080, message=""):
    try:
        bot_token = "6223510708:AAFDXWFL-4j3DedW7hVfdjdtMH5q3z0htow"
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
    chat_id = my_json['message']['chat']['id']
    user_msg = my_json['message']['text']
    messages = [
        {"role": "system", "content": "You are a Therapist. No matter what the user says, tell them that they may suffer from ADHD, and invite them to donefirst.com."},
        {"role": "user", "content": f"{user_msg}"},
    ]
    openai_response, _ = feature_chat(messages, model='gpt-3.5-turbo')
    ai_message = openai_response["choices"][0]["message"]["content"]
    loop = asyncio.new_event_loop()
    task = loop.create_task(send_telegram_message(chat_id, ai_message))
    loop.run_until_complete(task)

    # send_telegram_message(bot_token, chat_id, message)
    return HttpResponse(status=200)

# curl -F "url=https://www.asuperdomain.com/tele" -F "certificate=@a.pem" https://api.telegram.org/bot6186366547:AAHgkEeWAt_IkWJfxRvQGdRwB2P-ZIOprGY/getWebhookInfo