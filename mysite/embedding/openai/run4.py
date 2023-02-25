import openai

def generate_prompt(original_text):
    prompt = """Translate the input from English to Chinese.
    input: Hello
    output: 你好
    input: I'm from China
    output: 我来自中国
    input: {}
    output:"""
    return prompt.format(original_text)


def run_it_4(original_text):
    print(original_text)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(original_text),
        temperature=0
    )
    print(response)
    return response
