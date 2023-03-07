import df
import robot
import numpy as np


################################################################################
### Step 13
################################################################################
def run_it_2():
    my_text = """
        The job cuts in tech land are piling up, as companies that led the 10-year bull market adapt to a new reality.

Google announced plans to lay off 12,000 people from its workforce Friday, while Microsoft said Wednesday that it’s letting go of 10,000 employees. Amazon
 also began a fresh round of job cuts that are expected to eliminate more than 18,000 employees and become the largest workforce reduction in the e-retailer’s 28-year history.

The layoffs come in a period of slowing growth, higher interest rates to battle inflation, and fears of a possible recession next year.

Here are some of the major cuts in the tech industry so far. All numbers are approximations based on filings, public statements and media reports:

Alphabet: 12,000 jobs cut
Google, owned by parent company Alphabet, said Friday it will lay off 12,000 people from its workforce.

Sundar Pichai, Google’s CEO, said in an email sent to the company’s staff that the firm will begin making layoffs in the U.S. immediately. In other countries, the process “will take longer due to local laws and practices,” he said. CNBC reported in November that Google employees had been fearing layoffs as its counterparts made cuts and as employees saw changes to the company’s performance ratings system.

Alphabet
 had largely avoided layoffs until January, when it cut about 240 employees from Verily, its health sciences division.
 Microsoft: 10,000 jobs cut
Microsoft is reducing 10,000 workers through March 31 as the software maker braces for slower revenue growth. The company also is taking a $1.2 billion charge.

“I’m confident that Microsoft will emerge from this stronger and more competitive,” CEO Satya Nadella announced in a memo to employees that was posted on the company website Wednesday. Some employees will find out this week if they’re losing their jobs, he wrote.
Amazon: 18,000 jobs cut
Earlier this month, Amazon
 CEO Andy Jassy said the company was planning to lay off more than 18,000 employees, primarily in its human resources and stores divisions. It came after Amazon said in November it was looking to cut staff, including in its devices and recruiting organizations. CNBC reported at the time that the company was looking to lay off about 10,000 employees.

Amazon went on a hiring spree during the Covid-19 pandemic. The company’s global workforce swelled to more than 1.6 million by the end of 2021, up from 798,000 in the fourth quarter of 2019.

Crypto.com: 500 jobs cut
Crypto.com announced plans to lay off 20% of its workforce Jan. 13. The company had 2,450 employees, according to PitchBook data, suggesting around 490 employees were laid off. 

CEO Kris Marszalek said in a blog post that the crypto exchange grew “ambitiously” but was unable to weather the collapse of Sam Bankman-Fried’s crypto empire FTX without the further cuts.

“All impacted personnel have already been notified,” Marszalek said in a post.
"""

    my_texts = [("ss", my_text)]

    my_df = df.get_df(my_texts)
    my_df['embeddings'] = my_df['embeddings'].apply(eval).apply(np.array)
    qs = ["What day is it?",
          "Which company have laid off people?",
          "How many people are laid off by Amazon?",
          "How many people are laid off by Microsoft?",
          "Is layoff good or bad?",
          "How is Microsoft doing?",
          "How do patients like Done.?",
          "What's the relation between Crypto.com and Kris Marszalek?",
          "What did Kris Marszalek say in terms of layoff?"]
    for q in qs:
        print("Question:")
        print(q)
        print("Answer:")
        print(robot.answer_question(my_df, question=q))
        print("=======================\n\n\n")

run_it_2()