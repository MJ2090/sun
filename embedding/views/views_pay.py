from django.http import HttpResponse
from embedding.forms.grammar import GrammarForm
from embedding.openai.features import feature_grammar
from django.shortcuts import render
from embedding.utils import get_basic_data
import embedding.static_values as sc
import json
import stripe
from django.http import HttpResponseRedirect
from django.conf import settings as conf_settings


def pay_session(request):
    # prod
    stripe.api_key = conf_settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
            'name': 'T-shirt',
            },
            'unit_amount': 100,
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/pay_success',
    )
    return HttpResponseRedirect(session.url)


def pay(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/pay.html', ret)


def pay_success(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/pay_success.html', ret)