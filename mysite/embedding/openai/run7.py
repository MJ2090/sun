import openai


def run_it_7(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=1000
    )
    print(response)
    return response
