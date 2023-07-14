MODEL_TYPES_UNKNOWN = 0
MODEL_TYPES_EMBEDDING = 1
MODEL_TYPES_CHAT = 2
MODEL_TYPES_IMAGE = 3
MODEL_TYPES_TRANSLATE = 4
MODEL_TYPES_GRAMMAR = 5
MODEL_TYPES_SUMMARY = 6
MODEL_TYPES_QUIZ = 7
MODEL_TYPES = (
    (MODEL_TYPES_UNKNOWN, 'UNKNOWN'),
    (MODEL_TYPES_EMBEDDING, 'EMBEDDING'),
    (MODEL_TYPES_CHAT, 'CHAT'),
    (MODEL_TYPES_IMAGE, 'IMAGE'),
    (MODEL_TYPES_TRANSLATE, 'TRANSLATE'),
    (MODEL_TYPES_GRAMMAR, 'GRAMMAR'),
    (MODEL_TYPES_SUMMARY, 'SUMMARY'),
    (MODEL_TYPES_QUIZ, 'QUIZ'),
)

CHAT_TYPES_NO = 'Common AI'
CHAT_TYPES_TT1 = 'tt1'
CHAT_TYPES_ASSISTANT = 'Assistant'
CHAT_TYPES_PRESIDENT = 'Mr. President'
CHAT_TYPES_THERAPIST = 'Therapist'
CHAT_TYPES = (
    (CHAT_TYPES_NO, 'Common AI'),
    (CHAT_TYPES_TT1, 'TT 1'),
    (CHAT_TYPES_ASSISTANT, 'Virtual Assistant'),
    (CHAT_TYPES_PRESIDENT, 'Mr. President'),
    (CHAT_TYPES_THERAPIST, 'Therapist'),
)

TRAINING_MODELS_T = 'gpt-3.5-turbo'
TRAINING_MODELS_F = 'gpt-4'
TRAINING_MODELS_D = 'text-davinci-003'
TRAINING_MODELS_C = 'text-curie-001'
TRAINING_MODELS_A1 = 'ada:ft-personal-2023-03-01-22-16-31'
TRAINING_MODELS_C1 = 'curie:ft-personal:done-2023-03-01-23-56-55'
TRAINING_MODELS = (
    (TRAINING_MODELS_F, 'OpenAI GPT 4'),
    (TRAINING_MODELS_T, 'OpenAI GPT 3.5'),
    # (TRAINING_MODELS_D, 'OpenAI text model D'),
    # (TRAINING_MODELS_C, 'OpenAI text model C'),
    # (TRAINING_MODELS_A1, 'OpenAI fine tuning text model A1'),
    # (TRAINING_MODELS_C1, 'OpenAI fine tuning text model C1'),
)

QUIZ_MODELS_T = 'kuai'
QUIZ_MODELS_F = 'zhun'
QUIZ_MODELS = (
    (QUIZ_MODELS_T, '👩🏻‍🏫 Alice, expert of multiple choices'),
    (QUIZ_MODELS_F, '👨🏻‍💻 Bob, good at article writing'),
)

IMAGE_TYPES_DEFAULT = ''
IMAGE_TYPES_PICASSO = 'Picasso'
IMAGE_TYPES_MONET = 'Monet'
IMAGE_TYPES_VANGOGH = 'Vincent van Gogh'
IMAGE_TYPES_DALI = 'Salvador Dalí'
IMAGE_TYPES_MICHELANGELO = 'Michelangelo'
IMAGE_TYPES_COMICS = 'comics'
IMAGE_TYPES_BLACK_WHITE = 'black and white'
IMAGE_TYPES =(
    (IMAGE_TYPES_DEFAULT, 'Default style'),
    (IMAGE_TYPES_PICASSO, 'Picasso'),
    (IMAGE_TYPES_MONET, 'Monet'),
    (IMAGE_TYPES_VANGOGH, 'Vincent van Gogh'),
    (IMAGE_TYPES_DALI, 'Salvador Dalí'),
    (IMAGE_TYPES_MICHELANGELO, 'Michelangelo'),
    (IMAGE_TYPES_COMICS, 'comics'),
    (IMAGE_TYPES_BLACK_WHITE, 'black and white'),
)

TRANSLATION_CN = 'Chinese'
TRANSLATION_EN = 'English'
TRANSLATION_FR = 'French'
TRANSLATION_DE = 'German'
TRANSLATION_JP = 'Japanese'
TRANSLATION_KR = 'Korean'
TRANSLATION_SP = 'Spanish'
TRANSLATION_IT = 'Italien'
TRANSLATION_RU = 'Russie'
TRANSLATION_VE = 'Vietnamien'
TRANSLATION_PO = 'Português'
TRANSLATION_HE = 'Hebrew'
TRANSLATION_TYPES =(
    (TRANSLATION_CN, '中文'),
    (TRANSLATION_EN, 'English'),
    (TRANSLATION_FR, 'Français'),
    (TRANSLATION_DE, 'Deutsch'),
    (TRANSLATION_JP, 'やまと'),
    (TRANSLATION_KR, '한국어'),
    (TRANSLATION_SP, 'Español'),
    (TRANSLATION_IT, 'italiano'),
    (TRANSLATION_RU, 'русский язык'),
    (TRANSLATION_VE, 'Tiếng Việt'),
    (TRANSLATION_PO, 'Português'),
    (TRANSLATION_HE, 'עִברִית'),
)

IMAGE_COUNT_3 = 3
IMAGE_COUNT_6 = 6
IMAGE_COUNT_9 = 9
IMAGE_COUNTS = (
    (IMAGE_COUNT_3, 3),
    (IMAGE_COUNT_6, 6),
    (IMAGE_COUNT_9, 9),
)

Q_TYPE_1 = 'q_1'
Q_TYPE_2 = 'q_2'
Q_TYPES = (
    (Q_TYPE_1, 'Multiple choices'),
    (Q_TYPE_2, 'Article writing'),
)

QUESTION_LLM_TYPE_GPT = 'gpt-3.5-turbo-16k'
QUESTION_LLM_TYPE_GLM = 'glm'
QUESTION_LLM_TYPES =(
    (QUESTION_LLM_TYPE_GPT, 'GPT'),
    (QUESTION_LLM_TYPE_GLM, 'GLM'),
)

GAGA_TYPE_1 = 'wolfram + gpt4'
GAGA_TYPE_2 = 'wolfram + gpt3.5'
GAGA_TYPE_3 = 'pure gpt4'
GAGA_TYPE_4 = 'pure gpt3.5'
GAGA_TYPES = (
    (GAGA_TYPE_1, 'gpt 4 + wolfram'),
    (GAGA_TYPE_2, 'gpt 3.5 + wolfram'),
    (GAGA_TYPE_3, 'gpt 4 only'),
    (GAGA_TYPE_4, 'gpt 3.5 only'),
)