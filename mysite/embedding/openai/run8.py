import openai


def run_it_8(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    print(response)
    return response
