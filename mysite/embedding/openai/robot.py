import openai
import tiktoken
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity


def get_n_token(x):
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    print("okokok")
    return len(tokenizer.encode(x))

def create_context(question, df, max_len=1800):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():

        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4
        print('cur_len= ', cur_len, row['n_tokens'], row["text"], get_n_token(row["text"]))

        # If the context is too long, break
        if cur_len > max_len:
            break

        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    print('returns= ', max_len, len(returns), returns)
    return "\n\n###\n\n".join(returns)


def answer_question(
        df,
        model="gpt-3.5-turbo",
        question="Am I allowed to publish model outputs to Twitter, without a human review?",
        max_len=3600,
        debug=False,
        max_tokens=150,
        stop_sequence=None
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
    )
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the questin and context
        # my_prompt = f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:"
        system_prompt = f"Answer the question based on the context below, and if it can't be answered based on the context, say \"I don't know\""
        user_prompt = f"Context: {context}\n\n---\n\nQuestion: {question}\n\n---\n\nAnswer:"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        print('hahahahaah ', messages)
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0
        )
        # response = openai.Completion.create(
        #     prompt=my_prompt,
        #     temperature=0,
        #     max_tokens=max_tokens,
        #     top_p=1,
        #     frequency_penalty=0,
        #     presence_penalty=0,
        #     stop=stop_sequence,
        #     model=model,
        # )
        # return response["choices"][0]["text"].strip()
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(e)
        return ""