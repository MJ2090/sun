import embedding.openai.df as df
import embedding.openai.robot as robot


################################################################################
### Step 13
################################################################################
def run_it_3(my_text, qs):
    my_texts = [("embedding", my_text)]
    my_df = df.get_df(my_texts)
    ans = []
    for q in qs:
        tmp = {"Question": q, "Answer": robot.answer_question(my_df, question=q)}
        ans.append(tmp)

    print(ans)
    return ans
