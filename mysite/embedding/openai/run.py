import openai
import embedding.static_values as sc

def generate_prompt_6(original_text):
    prompt = """Generate the tl;dr for the input text.
    input: A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.
    output: Neutron stars are the collapsed cores of massive supergiant stars, with a radius of around 10 kilometres and a mass of 1.4 solar masses. They are formed from the supernova explosion of a massive star combined with gravitational collapse, compressing the core beyond white dwarf star density.
    input: {}
    output:"""
    return prompt.format(original_text)


def generate_prompt_5(original_text):
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

def generate_prompt_4(original_text):
    prompt = """Translate the input from English to Chinese.
    input: Hello
    output: 你好
    input: I'm from China
    output: 我来自中国
    input: {}
    output:"""
    return prompt.format(original_text)


def run_it_4(original_text, model):
    print(original_text)
    response = openai.Completion.create(
        model=model,
        prompt=generate_prompt_4(original_text),
        temperature=0,
        max_tokens=1000
    )
    print(model, generate_prompt_4(original_text))
    print(response)
    return response


def run_it_5(original_text, model):
    print(original_text)
    response = openai.Completion.create(
        model=model,
        prompt=generate_prompt_5(original_text),
        temperature=0,
        max_tokens=1000
    )
    print(response)
    return response


def run_it_6(original_text, model):
    response = openai.Completion.create(
        model=model,
        prompt=generate_prompt_6(original_text),
        temperature=0,
        max_tokens=1000
    )
    print(response)
    return response


def run_it_7(prompt, model):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,
        max_tokens=1000,
        stop=["###"]
    )
    print(response)
    return response


def run_it_8(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    print(response)
    return response


def run_it_9(messages, model):
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=1000,
        messages=messages,
    )
    print(response)
    return response