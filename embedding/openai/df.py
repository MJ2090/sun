import pandas as pd
import tiktoken
import openai
import numpy as np
import re

max_tokens_per_csv_line = 500


def remove_newlines(serie):
    serie = serie.str.replace('，', ',', regex=False)
    serie = serie.str.replace('。', '.', regex=False)
    serie = serie.str.replace('\r', ' ', regex=False)
    serie = serie.str.replace('\n', '', regex=False)
    # serie = serie.str.replace(' ', '', regex=False)
    serie = serie.str.replace('  ', ' ', regex=False)
    serie = serie.str.replace('   ', ' ', regex=False)
    serie = serie.str.replace('    ', ' ', regex=False)
    serie = serie.str.replace('\\n', ' ', regex=False)
    return serie


def generate_scraped_csv(my_texts=None):
    # Create a list to store the text files
    texts = my_texts
    # Create a dataframe from the list of texts
    df = pd.DataFrame(texts, columns=['fname', 'text'])
    # Set the text column to be the raw text with the newlines removed
    df['text'] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv('processed/scraped.csv')
    df.head()


# Splits the text into chunks of a maximum number of tokens
def split_into_many(text, tokenizer, max_tokens_per_csv_line=max_tokens_per_csv_line):
    # Split the text into sentences
    sentences = re.split('[\.]+[ ]*', text)

    # Get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence))
                for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        # If the number of tokens so far plus the number of tokens in the current sentence is greater
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far
        if tokens_so_far + token > max_tokens_per_csv_line:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # If the number of tokens in the current sentence is greater than the max number of
        # tokens, go to the next sentence
        # TODO: this may be a bug. we should not just simply drop the information.
        if token > max_tokens_per_csv_line:
            continue

        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks


def generate_embedding_csv():
    def myf(x):
        if pd.isna(x):
            return 0

        my_len = len(tokenizer.encode(x))
        return my_len

    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv('processed/scraped.csv', index_col=0, engine='python')
    df.text.replace(np.nan, "")
    df.dropna()
    df.columns = ['title', 'text']


    # Tokenize the text and save the number of tokens to a new column
    df['n_tokens'] = df.text.apply(myf)
    shortened = []
    # Loop through the dataframe
    for row in df.iterrows():
        # If the text is None, go to the next row
        if row[1]['text'] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]['n_tokens'] > max_tokens_per_csv_line:
            shortened += split_into_many(row[1]['text'], tokenizer)

        # Otherwise, add the text to the list of shortened texts
        else:
            shortened.append(row[1]['text'])

    df = pd.DataFrame(shortened, columns=['text'])
    df['n_tokens'] = df.text.apply(myf)

    # Note that you may run into rate limit issues depending on how many files you try to embed
    # Please check out our rate limit guide to learn more on how to handle this: https://platform.openai.com/docs/guides/rate-limits

    df['embeddings'] = df.text.apply(
        lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
    df.to_csv('processed/embeddings.csv')
    df.head()
    df = pd.read_csv('processed/embeddings.csv', index_col=0)
    df.head()

    return df


def get_df(my_texts=None):
    generate_scraped_csv(my_texts)
    return generate_embedding_csv()