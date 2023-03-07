import embedding.openai.df as df
import embedding.openai.robot as robot
import secrets
import string


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


def run_it_3_question(question, character):
    return "ssss"


def run_it_3_training(text):
    my_texts = [("embedding", text)]
    my_df = df.get_df(my_texts)
    file_name = ''.join(secrets.choice(
        string.ascii_uppercase + string.digits) for i in range(10))
    my_df.to_csv('processed_csv/' + file_name + '.csv')
    return file_name
