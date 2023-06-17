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
def tele(request):
    print("33333333333333333333300000000000000000000", request.POST, request.GET)
    return HttpResponse(json.dumps({'question': 'okk'}))

# curl -F "url=https://www.asuperdomain.com/tele" -F "certificate=@a.pem" https://api.telegram.org/bot6186366547:AAHgkEeWAt_IkWJfxRvQGdRwB2P-ZIOprGY/getWebhookInfo