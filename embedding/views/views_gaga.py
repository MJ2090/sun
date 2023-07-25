import wolframalpha
import openai
import json
from django.http import HttpResponse
from embedding.forms.gaga import GagaForm
from embedding.openai.features import feature_chat, feature_chat_with_function
from embedding.models import PromptModel
from django.shortcuts import render
from embedding.utils import record_dialogue, load_random_emoji, load_random_string, get_basic_data, record_consumption
import embedding.static_values as sc
from django.views.decorators.csrf import csrf_exempt
import stripe
import os

# model="gpt-3.5-turbo"
model = "gpt-4"
gpt_only = False


def get_my_function():
    query_description = """
The math query extracted from user message and sent to wolfram. 
sample input: 'we know x^2+x-6=0, what is x+100?' 
sample query: 'if x^2+x-6=0, what is x+100' 
sample input:'I have two books, Alice has 10 more, how many does Alice have?'
sample query: 'solve 2+10'
sample input: 'The cheese cost 3.5$, Bob paid 10$, how much change should he have?'
sample query: '10-3.5'
sample input: 'is 1999 a prime?'
sample query: 'is 1999 prime?'
sample input: 'tell if 2137 is exactly two times larger than 32'
sample output: '2137 = 2*32'
sample input: 'the hotel charges 50$ per night per person, additionally there is a 8% tax and a one-time checkin fee which is 11 per person. Alice & bob stayed there for 10 nights, how much is the total cost?'
sample output: '2 * ((50 * 10 * 1.08) + 11)'
sample input: 'i have 10 dollars, Alice has 324 more, how much do we have together?'
sample output: 'solve 10 + 432 + 10'
"""
    my_function = {
        "name": "get_math_answer",
        "description": "It calls wolfram API to find the correct answer to a math question.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": query_description
                }
            },
            "required": ["query"]
        }
    }
    return my_function


def get_query_or_answer(question, gpt_only=False):
    messages = [
        {"role": "system", "content": "You answer questions."},
        {"role": "user", "content": f"The question: {question}"},
    ]
    functions = [get_my_function()]
    if gpt_only:
        response = openai.ChatCompletion.create(
            model=model,
            temperature=0,
            max_tokens=1000,
            messages=messages,
        )
    else:
        response = openai.ChatCompletion.create(
            model=model,
            temperature=0,
            max_tokens=1000,
            messages=messages,
            functions=functions,
        )
    ai_response = response['choices'][0]['message']
    if "function_call" in ai_response:
        my_call = ai_response['function_call']
        if my_call['name'] == 'get_math_answer':
            params = json.loads(my_call['arguments'])
            return params['query'], None

    return None, ai_response['content']


def ask_one_question(question):
    question = question.strip()
    print("\n\nquestion:")
    print(question)
    query, gpt_answer = get_query_or_answer(question)
    if query:
        print("Rewritten Query:", query)
        wolfram_answer = get_math_answer(query)
        if wolfram_answer:
            final_ans = rephrase(question, wolfram_answer)
            print("Got Wolfram Answer:")
            print(final_ans)
            return final_ans
    print("Got GPT Answer:")
    print(gpt_answer)


def rephrase(question, answer_list):
    print("rephrase start:", question, answer_list)
    answer = '\n'.join(answer_list)
    base_prompt = f"""
There is a question and an answer, rephrase the answer so that it sounds more nature.
question: {question}
answer: {answer}
"""
    messages = [
        {"role": "system", "content": base_prompt},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0,
        max_tokens=1000,
        messages=messages,
    )
    ai_response = response['choices'][0]['message']['content']
    print("rephrased message:", ai_response)
    return ai_response


def get_math_answer(query):
    appid = "78U72L-P4W6T56RA5"
    client = wolframalpha.Client(appid)
    res = client.query(query)
    ans = []
    print("res==========\n", res)
    for pod in res.pods:
        print("we have title =====================", pod['@title'])
        if pod['@title'] in ['Solution over the reals', 'Results', 'Result', 'Exact result', 'Substitution']:
            for sub in pod.subpods:
                ans.append(sub.plaintext)
    return ans


def main():
    questions = [
        'sin(x)=x, x=?',
        'is 1999 a prime',
        'if (x+2)(x+3)=0, x=?',
        'I have 100 dollars, every day increate rate is 3%, how much will i have after 1 month?',
        'x^3+27=0, what is x',
        'sqrt(x)+190=x+178, what is x',
        'tell+if+2137+is+exactly two times larger than 32',
        "A small submarine started its dive at sea level and descended 30 feet per minute. Which integer represents the submarine's depth after seven minutes?",
        "Which represents the value of s in s + 12 >= 100? A. s > 88 B. s < 88 C. s = 88 D. s >= 88",
        "the hotel charges 250$ per night per person, additionally there is a 18% tax and a one-time checkin fee which is 110 per person. Alice, bob and I stayed there for 20 nights, how much is the total cost?",
    ]

    questions = [
        'what number is 10 times larger than the sum of 55 and 41?',
        'is 19997 a prime',
        'if (x+2)(x+3)=6, x=?',
        'I have 100 dollars, every month increate rate is 3%, how much will i have after 5 month?',
        'sqrt(6-x)= x, what is x',
        'what is the area of a rectangle which has width=32, height equals its double width?',
        'everyday i get 99 dollars but spend 39, how much do i have after 12 days?',
        "a flight a has gas tank of 9000 units, it costs 2 units per mile, how far can it fly",
        "Which represents the value of s in s + 43 = 43*9? A. s = 88 B. s = 188 C. s = 288 D. None of the above",
    ]
    for q in questions:
        ask_one_question(q)


def chat_async_gaga(request):
    new_message = request.POST['message']

    character = request.POST['character']
    if 'gpt4' in character:
        model = 'gpt-4'
    else:
        model = 'gpt-3.5-turbo'
    if 'wolfram' in character:
        gpt_only = False
    else:
        gpt_only = True

    dialogue_id = request.POST.get('dialogue_id', '')

    messages = json.loads(PromptModel.objects.get(name='gaga').history)
    history = request.POST.get('history')
    my_json = json.loads(history)
    messages.extend(my_json)
    messages.append({"role": "user", "content": new_message})

    if gpt_only:
        openai_response, request_time = feature_chat(messages, model=model)
    else:
        functions = [get_my_function()]
        openai_response, request_time = feature_chat_with_function(
            messages, model=model, functions=functions)

    ai_response = openai_response["choices"][0]["message"]
    ai_message = None
    rewritten_query = None
    if "function_call" in ai_response:
        my_call = ai_response['function_call']
        if my_call['name'] == 'get_math_answer':
            params = json.loads(my_call['arguments'])
            rewritten_query = params['query']
            print("Rewritten Query:", rewritten_query)
            wolfram_answer = get_math_answer(rewritten_query)
            if wolfram_answer:
                print("Got Wolfram Answer:", wolfram_answer)
                ai_message = rephrase(new_message, wolfram_answer)
    else:
        print("No function call ======================")

    if ai_message is None:
        ai_message = ai_response['content']
    print("ai_message============\n", ai_message)

    record_dialogue(request, 'User', new_message,
                    dialogue_id, 'gaga', request_time=request_time)
    record_dialogue(request, 'AI', ai_message, dialogue_id,
                    'gaga', request_time=request_time)

    return HttpResponse(json.dumps({'ai_message': ai_message, 'rewritten_query': rewritten_query}))


def chat_gaga(request):
    ret = get_basic_data(request)
    ret['hide_nav'] = True
    form = GagaForm()
    ret['form'] = form
    ret['welcome_word'] = 'Chat with Gagamia 👀'
    ret['ai_emoji'] = load_random_emoji()
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/gaga.html', ret)


@csrf_exempt
def gaga_pay_session(request):
    STRIPE_SECRET_KEY = os.environ["GAGA_STRIPE_SECRET_KEY"]
    if not STRIPE_SECRET_KEY:
        STRIPE_SECRET_KEY = "sk_test_51NOPgRK9OtnDAoGtqq3TBQZSV4wSoJ7Sz4RzPTSEMsenuBHo6xjE2O05ttTpy16L4duTOZKZ56PdLWeBGnrawjyw00FzMvjoqx"
    stripe.api_key = STRIPE_SECRET_KEY
    YOUR_DOMAIN = "https://localhost/"
    prod_id = request.POST.get("prod_id", "prod_1")
    if prod_id == "prod_1":
        price = 400
        name = "3 Months Membership"
    else:
        price = 49800
        name = "1 Year Membership"
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "cny",
                        "product_data": {
                            "name": name,
                            "images": [
                                "https://www.classgaga.com/images/mascot.png",
                            ],
                        },
                        "unit_amount": price,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success.html",
        )
    except Exception as e:
        print(e)
        return str(e)

    ret = {"url": checkout_session.url}
    return HttpResponse(json.dumps(ret))


def gagapay(request):
    return render(request, "embedding/gagapay.html", {})


@csrf_exempt
def gaga_intent(request):
    STRIPE_SECRET_KEY = os.environ["GAGA_STRIPE_SECRET_KEY"]
    if not STRIPE_SECRET_KEY:
        STRIPE_SECRET_KEY = "sk_test_51NOPgRK9OtnDAoGtqq3TBQZSV4wSoJ7Sz4RzPTSEMsenuBHo6xjE2O05ttTpy16L4duTOZKZ56PdLWeBGnrawjyw00FzMvjoqx"
    stripe.api_key = STRIPE_SECRET_KEY
    
    print("in request,", request.POST)
    prod_id = request.POST.get("prod_id", "prod_1")
    if prod_id == "prod_1":
        price = 400
        name = "3 Months Membership"
    else:
        price = 49800
        name = "1 Year Membership"

    intent = stripe.PaymentIntent.create(
        amount=price,
        currency="cny",
        payment_method_types=["alipay", "wechat_pay"],
    )
    print("intent=", intent)

    return HttpResponse(
        json.dumps(
            {
                "clientSecret": intent["client_secret"],
                "price": price,
            }
        )
    )