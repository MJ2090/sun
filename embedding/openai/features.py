import openai
import time
import embedding.static_values as sc
from embedding.llm import llama, glm
import embedding.openai.df as df
import embedding.openai.robot as robot
import secrets
import string
import pandas as pd
import os
import numpy as np

relative_path = '/var/www/asuperdomain.com/static/embedding/data/'


def get_embedding_prompt(question, random_str, model='gpt-3.5-turbo'):
    file_path = relative_path + random_str + '.csv'
    print(f"get_embedding_prompt: {file_path}", os.path.exists(file_path))
    if not os.path.exists(file_path):
        return "I don't know."
    my_df = pd.read_csv(file_path, index_col=0)
    my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    print("get_embedding_prompt, got df")
    return robot.get_glm_embedding_prompt(my_df, question=question)


def feature_question(question, random_str, model='gpt-3.5-turbo'):
    file_path = relative_path + random_str + '.csv'
    if not os.path.exists(file_path):
        return "I don't know."
    my_df = pd.read_csv(file_path, index_col=0)
    my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    if model == 'glm':
        ans = robot.answer_question_glm(my_df, question=question)
    else:
        ans = robot.answer_question_openai(my_df, question=question)
    return ans


def feature_action(question, model):
    msg = """
    A and B are talking with each other, if A says "{}", is it logically correct for B to reply as 
    "You can take the self assessment on our website"?
    Please only give a score between 1 and 100 and don't explain, where 1 means totally not possible, and 100 means very probably.
    """.format(question)
    messages = [
        {"role": "user", "content": msg},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0,
        max_tokens=1000,
        messages=messages,
    )

    return response


def feature_training(text):
    my_texts = [("embedding", text)]
    my_df = df.get_df(my_texts)
    my_df.head()
    random_str = ''.join(secrets.choice(
        string.ascii_uppercase + string.digits) for i in range(10))

    file_path = relative_path + random_str + '.csv'
    if not os.path.exists(relative_path):
        os.mkdir(relative_path)

    my_df.to_csv(file_path)

    my_df = pd.read_csv(file_path, index_col=0)
    return random_str


def feature_translate(original_text, target, model, stream=False):
    messages = [
        {"role": "system", "content": f"You are a helpful assistant that translates the original text to {target}."},
        {"role": "user", "content": f"Translate the following text to {target}: {original_text}"},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=2000,
        messages=messages,
        stream=stream,
    )
    return response


def feature_grammar(original_text, model):
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


def feature_summary(original_text, model):
    messages = [
        {"role": "system", "content": "Generate the tl;dr for the input text."},
        {"role": "user",
            "content": "A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei."},
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


def feature_image(prompt, count):
    response = openai.Image.create(
        prompt=prompt,
        n=count,
        size="256x256"
    )
    return response


def feature_chat_llama(request, messages, model):
    request_time = time.time()
    return llama.create(request, messages), request_time


def feature_glm(request, messages, prompt, temperature):
    request_time = time.time()
    return glm.create(request, messages, prompt, temperature), request_time


def feature_chat(messages, model):
    print(f"feature_chat with model {model}")
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


def feature_quiz(context, model="gpt-4", temperature=0.5):
    print(f"feature_quiz with model {model}")
    base_prompt = "有一段OCT识别产生的文字在「」内,可能包含一道或多道题目,按以下步骤处理:1,去掉与题目无关的文字.2,去掉缺失内容较多,无法作答的题目.3,整理剩下的题目,补上缺失,校正错字.4,解答.你的回答仅包含答案,不要输出别的内容,格式为'第1题: X\n第2题: Y.'."
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
