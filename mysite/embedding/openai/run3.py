import embedding.openai.df as df
import embedding.openai.robot as robot
import secrets
import string
import os


################################################################################
# Step 13
################################################################################
def run_it_3(my_text, qs):
    my_texts = [("embedding", my_text)]
    my_df = df.get_df(my_texts)
    ans = []
    for q in qs:
        tmp = {"Question": q, "Answer": robot.answer_question(
            my_df, question=q)}
        ans.append(tmp)

    print(ans)
    return ans


def run_it_3_question(question, random_str):
    file_path = 'processed_csv/' + random_str + '.csv'
    my_df = df.read_csv(file_path)
    ans = robot.answer_question(my_df, question=question)
    return ans


def run_it_3_training(text):
    my_texts = [("embedding", text)]
    my_df = df.get_df(my_texts)
    random_str = ''.join(secrets.choice(
        string.ascii_uppercase + string.digits) for i in range(10))
    
    file_path = 'processed_csv/' + random_str + '.csv'
    if not os.path.exists('processed_csv/'):
        os.mkdir('processed_csv')
    my_df.to_csv(file_path)
    return random_str
