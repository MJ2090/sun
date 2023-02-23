import df
import robot


################################################################################
### Step 13
################################################################################
def run_it_1():
    my_df = df.get_df()
    qs = ["What day is it?",
          "What is Done?",
          "What is ADHD?",
          "How to treat ADHD?",
          "How many people have ADHD?",
          "Where are you",
          "How do patients like Done.?"]
    for q in qs:
        print("Question:")
        print(q)
        print("Answer:")
        print(robot.answer_question(my_df, question=q))
        print("=======================")