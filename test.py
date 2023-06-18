from threading import Thread
from time import sleep
import pandas
import ast
import numpy as np


def threaded_function(arg):
    for i in range(arg):
        print("running")
        sleep(1)


def test2(question, embedding_model, llm_model='gpt-3.5-turbo-16k'):
    # def safe_literal_eval(value):
    #     try:
    #         return ast.literal_eval(value)
    #     except (ValueError, SyntaxError):
    #         return np.nan
    # relative_path = ''
    # file_path = relative_path + embedding_model.uuid + '.csv'
    # if not os.path.exists(file_path):
    #     return embedding_model.reject_message
    # my_df = pd.read_csv(file_path, index_col=0, nrows=5280).dropna()
    # print("333333333 1")
    # # my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    # my_df['embeddings'] = my_df['embeddings'].apply(safe_literal_eval).apply(np.array)
    # print("333333333 111")
    # if llm_model == 'glm':
    #     ans = robot.answer_question_glm(my_df, question=question)
    # else:
    #     ans = robot.answer_question_openai(
    #         my_df, question=question, debug=True, reject_message=embedding_model.reject_message)
    # return ans

if __name__ == "__main__":
    test2()