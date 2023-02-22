################################################################################
### Step 1
################################################################################

import os
import pandas as pd
import tiktoken
import openai
import numpy as np
import crawl

# Define root domain to crawl
domain = "www.donefirst.com"
full_url = "https://www.donefirst.com/company/our-mission"
max_tokens = 500


################################################################################
### Step 5
################################################################################

def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie

################################################################################
### Step 6
################################################################################


def generate_scraped_csv():
    # Create a list to store the text files
    texts = []

    # Get all the text files in the text directory
    for file in os.listdir("text/" + domain + "/"):
        # Open the file and read the text
        with open("text/" + domain + "/" + file, "r", encoding="UTF-8") as f:
            text = f.read()

            # Omit the first 11 lines and the last 4 lines, then replace -, _, and #update with spaces.
            texts.append((file[11:-4].replace('-', ' ').replace('_', ' ').replace('#update', ''), text))

    # Create a dataframe from the list of texts
    print(texts)
    print("enddd")
    df = pd.DataFrame(texts, columns=['fname', 'text'])

    # Set the text column to be the raw text with the newlines removed
    df['text'] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv('processed/scraped.csv')
    df.head()

def generate_scraped_csv_2(my_texts):
    # Create a list to store the text files
    texts = my_texts

    # # Get all the text files in the text directory
    # for file in os.listdir("text/" + domain + "/"):
    #     # Open the file and read the text
    #     with open("text/" + domain + "/" + file, "r", encoding="UTF-8") as f:
    #         text = f.read()
    #
    #         # Omit the first 11 lines and the last 4 lines, then replace -, _, and #update with spaces.
    #         texts.append((file[11:-4].replace('-', ' ').replace('_', ' ').replace('#update', ''), text))

    # Create a dataframe from the list of texts
    df = pd.DataFrame(texts, columns=['fname', 'text'])

    # Set the text column to be the raw text with the newlines removed
    df['text'] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv('processed/scraped.csv')
    df.head()


################################################################################
### Step 8
################################################################################


# Function to split the text into chunks of a maximum number of tokens
def split_into_many(text, tokenizer, max_tokens=max_tokens):
    # Split the text into sentences
    sentences = text.split('. ')

    # Get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        # If the number of tokens so far plus the number of tokens in the current sentence is greater
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # If the number of tokens in the current sentence is greater than the max number of
        # tokens, go to the next sentence
        if token > max_tokens:
            continue

        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks


def generate_embedding_csv():
    ################################################################################
    ### Step 7
    ################################################################################

    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv('processed/scraped.csv', index_col=0)
    df.columns = ['title', 'text']

    # Tokenize the text and save the number of tokens to a new column
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    # Visualize the distribution of the number of tokens per row using a histogram
    df.n_tokens.hist()
    shortened = []

    # Loop through the dataframe
    for row in df.iterrows():

        # If the text is None, go to the next row
        if row[1]['text'] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]['n_tokens'] > max_tokens:
            shortened += split_into_many(row[1]['text'], tokenizer)

        # Otherwise, add the text to the list of shortened texts
        else:
            shortened.append(row[1]['text'])

    ################################################################################
    ### Step 9
    ################################################################################

    df = pd.DataFrame(shortened, columns=['text'])
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    df.n_tokens.hist()

    ################################################################################
    ### Step 10
    ################################################################################

    # Note that you may run into rate limit issues depending on how many files you try to embed
    # Please check out our rate limit guide to learn more on how to handle this: https://platform.openai.com/docs/guides/rate-limits

    df['embeddings'] = df.text.apply(
        lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
    df.to_csv('processed/embeddings.csv')
    df.head()

    ################################################################################
    ### Step 11
    ################################################################################

    df = pd.read_csv('processed/embeddings.csv', index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

    df.head()

    return df


def get_df():
    crawl.crawl(full_url)
    generate_scraped_csv()
    return generate_embedding_csv()


def get_df_2():
    my_text="""
    ADHD: A four-letter acronym that stands for attention-deficit/hyperactivity disorder. Across our society and throughout modern history, it has also come to represent harmful stereotypes, debilitating assumptions, and unconscious bias.

Our mission is to empower everyone living with ADHD to reach their fullest potential. We meet that mission by providing a patient-first, technology-powered ADHD treatment platform that keeps costs down and reduces patient wait times.

Unchecked and untreated, ADHD can hamper brain development and impede everything from a person’s social skills to their productivity in a professional environment. While the condition itself is considered very common, with more than 3 million cases now diagnosed annually in the U.S. alone, the treatment opportunities for ADHD are anything but common. Most people suffer in silence.

We are facing a challenge when it comes to providing psychiatric care, physician burnout, an aging workforce, bureaucratic and insurance demands, and poor compensation. In fact, it’s a simple math equation. In total, more than 20 million people in the U.S. have received a diagnosis of ADHD. But there are fewer than 30,000 psychiatrists to treat them. That means there are roughly 667 patients per psychiatrist. Clearly, unsustainable.

Beyond addressing the emotional and mental wellness of patients we also see an opportunity to address the financial impact of $150-200 million in lost productivity every year due to ADHD. In addition, no one should lose their job over ADHD, and no one should lose their opportunity to find a meaningful path forward in their professional life as well as their personal one.

Clearly, the time is now to change the course of this treatable condition. The solution?

At Done., first we want to eliminate the stigma and confusion or isolation around ADHD and empower anyone to receive the help they need to live up to their fullest potential. We provide awareness and education for people to learn more, confidential and accurate medical diagnosis through telehealth, and actionable ways to receive immediate treatment.

We’ve also hired some of the most esteemed and board-certified experts in the industry to collaborate and tackle ADHD together. Their wisdom and experience has allowed us to build a robust online platform that infuses efficiency with effectiveness. We put the patient’s needs first and seek to provide a stable scaffolding during their entire journey with us.

Done. is dedicated to serving individuals who otherwise may not be comfortable seeking care for ADHD in person due to stigma around ADHD treatment or may not be able to access care due to cost or availability.   By providing a platform that deals directly with patients and manages the logistics and administrative work around their care, Done. allows providers to spend more time focusing on what they do best – evaluating and treating patients.

Indeed, we believe that technology is a vital part of the solution to connect anyone to the right psychiatric care at the right time - even through their mobile device. This “always-on” strategy allows for seamless accessibility, convenient interactions like video calls, and 24/7 support. Our patients are the lifeblood of Done. and we know that the overwhelming nature of ADHD can strike at any moment.

There is also a shared responsibility between the patient, the medical practitioner, and Done. to ensure everyone receives responsible and quality treatment in such a timely manner. That treatment can include therapy, medication, or a combination of options depending on the circumstances.

Done. does not generate the diagnosis. Rather Done. serves as the ultimate conduit between ailment and treatment; Done.’s clinical operations are managed by an independent professional corporation (PC) headed by board-certified psychiatrists and psychiatric mental health nurse practitioners.

Our approach is simple:

1. Visit donefirst.com to take a medically approved assessment test and learn where a patient falls in the spectrum of ADHD (80% of adults with ADHD are not even aware).

2. Schedule an appointment directly with a medical practitioner and for a patient to discuss their wellness in private.

3. Once treatment is determined, a patient has the option to join Done. as a valued member of our services and access a broad network of clinicians.

Of course we do not suggest that our approach is perfect. No medical system in the world functions without difficulties and hurdles along the way. But we know it’s working.
    """
    generate_scraped_csv_2(["asdf", my_text])
    return generate_embedding_csv()
