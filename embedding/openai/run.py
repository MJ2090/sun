import openai
import embedding.static_values as sc
from embedding.llm import llama, glm


def run_it_translate(original_text, target, model):
    messages = [
        {"role": "system", "content": f"You are a helpful assistant that translates the original text to {target}."},
        {"role": "user", "content": f"Translate the following text to {target}: {original_text}"},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=2000,
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

    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.2,
        max_tokens=3000,
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
        max_tokens=3000,
        messages=messages,
    )
    return response


def run_it_7(prompt, model):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,
        max_tokens=3000,
        stop=["###"]
    )
    return response


def run_it_image(prompt, count):
    response = openai.Image.create(
        prompt=prompt,
        n=count,
        size="256x256"
    )
    return response


def run_it_chat_llama(request, messages, model):
    return llama.create(request, messages)


def run_it_glm(request, messages, prompt):
    return glm.create(request, messages, prompt)


def run_it_chat(messages, model):
    print(f"run_it_chat with model {model}")
    try:
        response = openai.ChatCompletion.create(
            model=model,
            temperature=0.5,
            max_tokens=3300,
            messages=messages,
        )
        return response
    except openai.error.Timeout as e:
        print(f"OpenAI API request timed out: {e} with message {messages}")
        return "Sorry it was time out :D"
    

def run_it_quiz(context, model="gpt-4"):
    print(f"run_it_quiz with model {model}")
    base_prompt="给你这样一段文字放在「」内,这段文字是通过ocr从照片或者截屏中获取的,这段文字包含一道或多道题目,你需要通过以下步骤来处理这段文字:第一步,把不属于题目内容的多余文字去掉.第二步:把缺失内容较多,导致无法作答的题目去掉.第三步:整理剩下的题目,补上缺失的文字,校正ocr识别出错的文字.第四步:给出答案,答案格式为'第几题: 答案, 第几题: 答案.'."
    messages = [
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": f"需要你处理的文字为「{context}」"},
    ]
    print(f'promot: {messages}')
    try:
        response = openai.ChatCompletion.create(
            model=model,
            temperature=0.9,
            max_tokens=1500,
            messages=messages,
        )
        return response
    except openai.error.Timeout as e:
        print(f"OpenAI API request timed out: {e} with message {messages}")
        return "Sorry it was time out :D"