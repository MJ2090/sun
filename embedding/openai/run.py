import openai
import time
import embedding.static_values as sc
from embedding.llm import llama, glm


def run_it_translate(original_text, target, model):
    messages = [
        {"role": "system", "content": f"You are a helpful assistant that translates the original text to {target}."},
        {"role": "user", "content": f"Translate the following text to {target}: {original_text}"},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=2000,
        messages=messages,
    )
    return response


def run_it_grammar(original_text, model):
    messages = [
        {"role": "system", "content": "You correct the input text to standard English, fix all the misspelled words, grammatical and syntax errors."},
        {"role": "user", "content": "How old is you?"},
        {"role": "assistant", "content": "How old are you?"},
        {"role": "user", "content": "She no went to the market."},
        {"role": "assistant", "content": "She did not go to the market."},
        {"role": "user", "content": "Please wait me! I are coming son!"},
        {"role": "assistant", "content": "Please wait for me! I am coming soon!"},
        {"role": "user", "content": "When yoo misspell smething, you spell it worng."},
        {"role": "assistant", "content": "When you misspell something, you spell it wrong."},
        {"role": "user", "content": "{}".format(original_text)},
    ]

    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=3000,
        messages=messages,
    )
    return response


def run_it_summary(original_text, model):
    messages = [
        {"role": "system", "content": "Generate the tl;dr for the input text."},
        {"role": "user", "content": "A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei."},
        {"role": "assistant", "content": "Neutron stars are the collapsed cores of massive supergiant stars, with a radius of around 10 kilometres and a mass of 1.4 solar masses. They are formed from the supernova explosion of a massive star combined with gravitational collapse, compressing the core beyond white dwarf star density."},
        {"role": "user", "content": "{}".format(original_text)},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=3000,
        messages=messages,
    )
    return response


def run_it_7(prompt, model):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,
        max_tokens=3000,
        stop=["###"]
    )
    return response


def run_it_image(prompt, count):
    response = openai.Image.create(
        prompt=prompt,
        n=count,
        size="256x256"
    )
    return response


def run_it_chat_llama(request, messages, model):
    request_time = time.time()
    return llama.create(request, messages), request_time


def run_it_glm(request, messages, prompt, temperature):
    request_time = time.time()
    return glm.create(request, messages, prompt, temperature), request_time


def run_it_chat(messages, model):
    print(f"run_it_chat with model {model}")
    request_time = time.time()
    try:
        response = openai.ChatCompletion.create(
            model=model,
            temperature=0.6,
            max_tokens=2000,
            messages=messages,
        )
        return response, request_time
    except openai.error.Timeout as e:
        print(f"OpenAI API request timed out: {e} with message {messages}")
        return "Sorry it was time out :D", request_time
    

def run_it_quiz(context, model="gpt-4", temperature=0.5):
    print(f"run_it_quiz with model {model}")
    base_prompt="有一段OCT识别产生的文字在「」内,可能包含一道或多道题目,按以下步骤处理:1,去掉与题目无关的文字.2,去掉缺失内容较多,无法作答的题目.3,整理剩下的题目,补上缺失,校正错字.4,解答,格式为'第几题: 答案\n第几题: 答案.'."
    messages = [
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": f"需处理的文字:「{context}」"},
    ]
    print(f'promot: {messages}')
    request_time = time.time()
    try:
        response = openai.ChatCompletion.create(
            model=model,
            temperature=temperature,
            max_tokens=1500,
            messages=messages,
        )
        return response, request_time
    except openai.error.Timeout as e:
        print(f"OpenAI API request timed out: {e} with message {messages}")
        return "Sorry it was time out :D", request_time