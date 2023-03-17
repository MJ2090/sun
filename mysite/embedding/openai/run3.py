import embedding.openai.df as df
import embedding.openai.robot as robot
import secrets
import string
import pandas as pd
import os
import numpy as np
import openai

relative_path = '/var/www/asuperdomain.com/static/embedding/data/'


################################################################################
# Step 13
################################################################################
def run_it_3(my_text, qs):
    my_texts = [("embedding", my_text)]
    my_df = df.get_df(my_texts)
    my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    ans = []
    for q in qs:
        tmp = {"Question": q, "Answer": robot.answer_question(
            my_df, question=q)}
        print('originalllllll', my_df, q)
        ans.append(tmp)

    print(ans)
    return ans


def run_it_3_question(question, random_str):
    file_path = relative_path + random_str + '.csv'
    my_df = pd.read_csv(file_path, index_col=0)
    my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    ans = robot.answer_question(my_df, question=question)
    return ans

def run_it_3_action(question, model):
    msg = """
    A and B are talking with each other, if A says "{}", is it logically correct for B to reply as “You can take the self assessment on our website”? Please only give a score between 1 and 10 and don't explain, where 1 means totally not possible, and 10 means very probably.
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
    response = response.replace('.', '')
    print('run_it_3_action ', response)
    if response.isnumeric() and int(response)>8:
        return 1
    return 0


def run_it_3_training(text):
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
