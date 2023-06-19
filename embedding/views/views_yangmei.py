from django.http import HttpResponse
from django.shortcuts import render
from embedding.utils import get_basic_data
import json
from datetime import datetime
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings


@csrf_exempt
def yangmei_intent(request):
    stripe.api_key = conf_settings.STRIPE_SECRET_KEY
    
    intent = stripe.PaymentIntent.create(
        amount=700,
        currency='cny',
        payment_method_types=['alipay', 'wechat_pay']
    )
    return HttpResponse(json.dumps({
        'clientSecret': intent['client_secret']
    }))


def yangmei_async(request):
    username = ''
    uuid = ''
    type = ''
    quantity = 0
    return HttpResponse(json.dumps({'username': username, 'uuid': uuid, 'type': type, 'quantity': quantity}))


def yangmei(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/yangmei.html', ret)
