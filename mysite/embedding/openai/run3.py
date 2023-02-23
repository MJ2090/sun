import embedding.openai.df
import embedding.openai.robot
import sys


################################################################################
### Step 13
################################################################################
def run_it_3(my_text, qs):
    my_texts = [("ss", my_text)]
    print(sys.path)

    my_df = embedding.openai.df.get_df(my_texts)
    ans = []
    for q in qs:
        ans.append("Question:")
        ans.append(q)
        ans.append("Answer:")
        ans.append(robot.answer_question(my_df, question=q))
        ans.append("=======================\n\n\n")

    print("\n".join(ans))
    return ans
