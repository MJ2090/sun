import openai

def generate_prompt(original_text):
    prompt = """Correct the input text to standard English, fix all the misspelled words, grammatical errors and syntax errors.
    input: How old is you?
    output: How old are you?
    input: She no went to the market.
    output: She did not go to the market.
    input: Please wait me! I are coming son!
    output: Please wait for me! I am coming soon!
    input: When yoo misspell smething, you spell it worng.
    output: When you misspell something, you spell it wrong.
    input: {}
    output:"""
    return prompt.format(original_text)


def run_it_5(original_text):
    print(original_text)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(original_text),
        temperature=0,
        max_tokens=1000
    )
    print(response)
    return response
