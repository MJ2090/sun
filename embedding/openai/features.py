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
from django.conf import settings as conf_settings
import tiktoken
import ast
from numpy import nan

relative_path = conf_settings.EMBEDDING_DIR


def get_embedding_prompt(question, random_str, model='gpt-3.5-turbo'):
    file_path = relative_path + random_str + '.csv'
    print(f"get_embedding_prompt: {file_path}", os.path.exists(file_path))
    if not os.path.exists(file_path):
        return "I don't know."
    my_df = pd.read_csv(file_path, index_col=0)
    my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    print("get_embedding_prompt, got df")
    return robot.get_glm_embedding_prompt(my_df, question=question)


def feature_add_embedding_doc(embedding_model, openai_response):
    csv_origin = relative_path + embedding_model.uuid + '.csv'
    csv_addition = relative_path + openai_response + '.csv'
    print("feature_add_embedding_doc", openai_response)
    df = pd.DataFrame()
    for file in [csv_origin, csv_addition]:
        data = pd.read_csv(file)
        df = pd.concat([df, data], axis=0)
    df.to_csv(csv_origin, index=False)


def feature_question(question, embedding_model, llm_model='gpt-3.5-turbo-16k'):
    file_path = relative_path + embedding_model.uuid + '.csv'
    if not os.path.exists(file_path):
        return embedding_model.reject_message
    my_df = pd.read_csv(file_path, index_col=0)
    print("333333333 1")
    from numpy import nan
    my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    # my_df['embeddings'] = my_df['embeddings'].apply(ast.literal_eval)
    print("333333333 111")
    if llm_model == 'glm':
        ans = robot.answer_question_glm(my_df, question=question)
    else:
        ans = robot.answer_question_openai(
            my_df, question=question, debug=True, reject_message=embedding_model.reject_message)
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
        os.makedirs(relative_path)

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
        max_tokens=1500,
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
        {"role": "user", "content": "{}".format(original_text)},
    ]

    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=1500,
        messages=messages,
    )
    return response


def feature_summary(original_text, model='gpt-3.5-turbo-16k', max_words=0, max_tokens=1500):
    original_text = original_text.replace('\n', '')
    n_tokens = count_tokens(original_text, model)
    token_limit = 12000
    if n_tokens > token_limit:
        original_len = len(original_text)
        original_text = original_text[:original_len * 12000 // n_tokens]
        print("===========================\nn_tokens exceeded 12000: ", n_tokens)
        print("after truncation: n_tokens =",
              count_tokens(original_text, model))
    messages = [
        {"role": "system", "content": "Summarize the Input Text. Step #1. determine which language is used in the Input Text. Step #2. write a summary based on the Input Text in the same language."},
        {"role": "user", "content": "The Output MUST only contains the summary. The summary MUST use the same language as the input text."},
        {"role": "user", "content": f"Input Text:\n\n\n {original_text}."},
    ]
    if max_words > 0:
        messages[0]['content'] += f" The summary MUST be within {max_words} words."
    try:
        print("model: ", model)
        print("Msg sent to openai: ", messages)

        response = openai.ChatCompletion.create(
            model=model,
            temperature=0.2,
            max_tokens=max_tokens,
            messages=messages,
        )
        print("Msg from openai: ", response)
    except openai.error.InvalidRequestError as e:
        print(f"OpenAI API request InvalidRequestErro, retry #1..\n: {e}")
        half_len = len(original_text)//2
        # original_text = original_text[:half_len]
        messages[2]["content"] = f"Input Text:\n\n\n {original_text}"
        print("Msg sent to openai: ", messages)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.2,
            max_tokens=max_tokens,
            messages=messages,
        )
        print("Msg from openai: ", response)
        return response

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


def feature_chat(messages, model, retry=0):
    request_time = time.time()
    try:
        print(f"\nfeature_chat with model {model}")
        print("\nMsg sent to openai: ", messages)
        response = openai.ChatCompletion.create(
            model=model,
            temperature=0.9,
            max_tokens=1500,
            messages=messages,
        )
        print("\nMsg returned from openai: ", response)
        return response, request_time
    except openai.error.Timeout as e:
        print(f"OpenAI API request timed out: {e} with message {messages}")
        return "Sorry it was time out :D", request_time
    except openai.error.APIError as e:
        print(f"OpenAI API request APIerror: {e} with message {messages}")
        if retry == 0:
            return feature_chat(messages, model, retry=1)
        else:
            return "ERROR IN OEPNAI API"


def feature_quiz(context, model="gpt-4", temperature=0.5, q_type=''):
    messages = get_quiz_prompt(q_type=q_type, context=context)
    request_time = time.time()
    try:
        print(f"Msg sent to openai {model}: {messages}")
        response = openai.ChatCompletion.create(
            model=model,
            temperature=temperature,
            max_tokens=1500,
            messages=messages,
        )
        print(f"Msg from openai {model}: {response}")
        return response, request_time
    except openai.error.Timeout as e:
        print(f"OpenAI API request timed out: {e} with message {messages}")
        return "ERROR", request_time
    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        return "ERROR", request_time
    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        return "ERROR", request_time
    except openai.error.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        return "ERROR", request_time
    except openai.error.InvalidRequestError as e:
        # Handle InvalidRequestError
        print(f"OpenAI API request is invalid: {e}")
        return "ERROR", request_time


def get_quiz_prompt(q_type='', context=''):
    if q_type == 'q_1':
        base_prompt = "有一段OCT识别产生的文字在「」内,可能包含一道或多道选择题或判断题,按以下步骤处理:1,去掉与题目无关的文字.2,去掉缺失内容较多,无法作答的题目.3,整理剩下的题目,补上缺失,校正错字.4,解答.你的回答仅包含答案,不要输出别的内容,格式为'第1题: X\n第2题: Y.'. 如果无法找到选择题或判断题, 返回'无法找到选择或判断题 请给出更清晰的描述'"
        messages = [
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": f"需处理的文字:「{context}」"},
        ]
        return messages
    if q_type == 'q_2':
        base_prompt = "有一段文字在「」内,可能包含一道或多道问答题或者论述题. 整理并找到这些问答题或论述题, 如果无法找到, 返回'无法回答 请给出更清晰的问题描述', 如果能找到, 解答这些题目. "
        messages = [
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": f"需处理的文字:「{context}」"},
        ]
        return messages
    base_prompt = "有一段OCT识别产生的文字在「」内,可能包含一道或多道题目,按以下步骤处理:1,去掉与题目无关的文字.2,去掉缺失内容较多,无法作答的题目.3,整理剩下的题目,补上缺失,校正错字.4,解答.你的回答仅包含答案,不要输出别的内容,格式为'第1题: X\n第2题: Y.'."
    messages = [
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": f"需处理的文字:「{context}」"},
    ]
    return messages


def count_tokens(message, model):
    encoding = tiktoken.get_encoding("cl100k_base")
    count = len(encoding.encode(message))
    return count
