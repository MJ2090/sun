import openai
import embedding.static_values as sc


def run_it_translate(original_text, target, model):
    messages = [
        {"role": "system", "content": f"You are a helpful assistant that translates the original text to {target}."},
        {"role": "user", "content": f"Translate the following text to {target}: {original_text}"},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=4000,
        messages=messages,
    )
    return response


def run_it_grammar(original_text, model):
    messages = [
        {"role": "system", "content": "You correct the input text to standard English, fix all the misspelled words, grammatical and syntax errors."},
        {"role": "user", "content": "How old is you?"},
        {"role": "assistant", "content": "How old are you?"},
        {"role": "user", "content": "She no went to the market."},
        {"role": "assistant", "content": "She did not go to the market."},
        {"role": "user", "content": "Please wait me! I are coming son!"},
        {"role": "assistant", "content": "Please wait for me! I am coming soon!"},
        {"role": "user", "content": "When yoo misspell smething, you spell it worng."},
        {"role": "assistant", "content": "When you misspell something, you spell it wrong."},
        {"role": "user", "content": "{}".format(original_text)},
    ]

    print(original_text)
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=4000,
        messages=messages,
    )
    return response


def run_it_summary(original_text, model):
    messages = [
        {"role": "system", "content": "Generate the tl;dr for the input text."},
        {"role": "user", "content": "A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei."},
        {"role": "assistant", "content": "Neutron stars are the collapsed cores of massive supergiant stars, with a radius of around 10 kilometres and a mass of 1.4 solar masses. They are formed from the supernova explosion of a massive star combined with gravitational collapse, compressing the core beyond white dwarf star density."},
        {"role": "user", "content": "{}".format(original_text)},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=4000,
        messages=messages,
    )
    return response


def run_it_7(prompt, model):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,
        max_tokens=4000,
        stop=["###"]
    )
    return response


def run_it_8(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response


def run_it_9(messages, model):
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=4000,
        messages=messages,
    )
    return response
