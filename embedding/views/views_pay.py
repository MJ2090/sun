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
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def stripe_call(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret = 'whsec_6ajYwJ2I4sNhrIKuDHBWf0FyHjDllUry'

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    print(event, event['type'])
    return HttpResponse(status=200)


def pay_session(request):
    stripe.api_key = conf_settings.STRIPE_SECRET_KEY
    # stripe.api_key = "sk_test_GwtC7lzItVuVtgBPc6KQPS7N"
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'A.I',
                },
                'unit_amount': 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://asuperdomain.com/pay_success',
    )
    print(session)
    return HttpResponseRedirect(session.url)


def pay(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/pay.html', ret)


def pay_success(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/pay_success.html', ret)
