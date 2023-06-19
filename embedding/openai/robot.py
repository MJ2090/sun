import openai
from openai.embeddings_utils import distances_from_embeddings


def create_context(question, df, max_len=1800):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(
        input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(
        q_embeddings, df['embeddings'].values, distance_metric='cosine')

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4
        # If the context is too long, break
        if cur_len > max_len:
            break
        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    return "\n\n###\n\n".join(returns)


def answer_question_openai(
        df,
        model="gpt-3.5-turbo-16k",
        question="Am I allowed to publish model outputs to Twitter, without a human review?",
        max_len=12000,
        debug=False,
        reject_message="No Answer"
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

    try:
        system_prompt = f"Answer the question based on the context below. If it can't be answered based on the context, say exactly \"{reject_message}\". Write the answer in the same language as the question. Do not miss any points in the context. If asked who you are, NEVER mention GPT or Openai, your name is AI Assistant."
        user_prompt = f"Context: {context}\n\n---\n\nQuestion: {question}\n\n---\n\nAnswer:"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        if debug:
            print(f"Msg sent to openai:\n{messages}\n\n")
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.8
        )
        if debug:
            print(f"Msg returned from openai:\n{response}\n\n")
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(e)
        return ""


def get_glm_embedding_prompt(
        df,
        question="Am I allowed to publish model outputs to Twitter, without a human review?",
        max_len=3600,
        debug=False
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    print("get_glm_embedding_prompt, start", question)
    context = create_context(
        question,
        df,
        max_len=max_len,
    )
    print("get_glm_embedding_prompt, end")
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    system_prompt = f"根据下文提供的内容回答问题. 如果无法从下文中得到答案, 回答 我不知.\n\n内容: {context}\n\n问题: {question}"
    return system_prompt
