from django.http import HttpResponse
from django.shortcuts import render
from embedding.utils import get_basic_data
from django.utils.translation import activate
import json
from datetime import datetime
import stripe
from embedding.models import FruitOrder
from django.conf import settings as conf_settings
import time
from embedding.utils import load_random_number_string


def yangmei_intent(request):
    print("in request,", request.POST)
    stripe.api_key = conf_settings.STRIPE_SECRET_KEY
    t_name = request.POST.get('t_name', '')
    t_size = request.POST.get('t_size', '')
    t_address = request.POST.get('t_address', '')
    t_area = request.POST.get('t_area', '')
    t_quantity = int(request.POST.get('t_quantity', 0))
    t_mobile = request.POST.get('t_mobile', '')
    t_notes = request.POST.get('t_notes', '')
    order_id = load_random_number_string(8)

    price = calc_price(t_size, t_quantity, t_area)
    intent = stripe.PaymentIntent.create(
        amount=price * 100,
        currency='cny',
        payment_method_types=['alipay', 'wechat_pay']
    )
    print("intent=", intent)
    current_time = time.time()
    FruitOrder.objects.create(username=t_name,
                              area=t_area,
                              mobile=t_mobile,
                              address=t_address,
                              notes=t_notes,
                              size=t_size,
                              pi_id=intent['id'],
                              created_time=current_time,
                              quantity=t_quantity,
                              order_id=order_id,
                              price=price,
                              order_state='new',
                              )

    return HttpResponse(json.dumps({
        'clientSecret': intent['client_secret'], 'price': price
    }))


def calc_price(t_size, t_quantity, t_area):
    if t_size == '1':
        base_price = 140
    else:
        base_price = 60
    area_price = {'1': 20, '2': 20, '3': 20, '4': 20, '5': 20, '6': 20, '7': 20, '8': 20, '9': 20}
    if t_area in area_price:
        base_price += area_price[t_area]
    
    return base_price * t_quantity


def yangmei_async(request):
    username = ''
    uuid = ''
    type = ''
    quantity = 0
    return HttpResponse(json.dumps({'username': username, 'uuid': uuid, 'type': type, 'quantity': quantity}))


def yangmei(request):
    user_language = "zh_hans"
    activate(user_language)
    ret = get_basic_data(request, {'hide_nav': True})
    return render(request, 'embedding/yangmei.html', ret)
