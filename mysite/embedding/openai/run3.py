import embedding.openai.df
import robot


################################################################################
### Step 13
################################################################################
def run_it_3(my_text, qs):
    my_texts = [("ss", my_text)]

    my_df = df.get_df(my_texts)
    for q in qs:
        print("Question:")
        print(q)
        print("Answer:")
        print(robot.answer_question(my_df, question=q))
        print("=======================\n\n\n")


run_it_3()