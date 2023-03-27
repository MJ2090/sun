MODEL_TYPES_UNKNOWN = 0
MODEL_TYPES_EMBEDDING = 1
MODEL_TYPES_CHAT = 2
MODEL_TYPES_IMAGE = 3
MODEL_TYPES_TRANSLATE = 4
MODEL_TYPES_GRAMMAR = 5
MODEL_TYPES_SUMMARY = 6
MODEL_TYPES = (
    (MODEL_TYPES_UNKNOWN, 'UNKNOWN'),
    (MODEL_TYPES_EMBEDDING, 'EMBEDDING'),
    (MODEL_TYPES_CHAT, 'CHAT'),
    (MODEL_TYPES_IMAGE, 'IMAGE'),
    (MODEL_TYPES_TRANSLATE, 'TRANSLATE'),
    (MODEL_TYPES_GRAMMAR, 'GRAMMAR'),
    (MODEL_TYPES_SUMMARY, 'SUMMARY'),
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
TRAINING_MODELS_D = 'text-davinci-003'
TRAINING_MODELS_C = 'text-curie-001'
TRAINING_MODELS_A1 = 'ada:ft-personal-2023-03-01-22-16-31'
TRAINING_MODELS_C1 = 'curie:ft-personal:done-2023-03-01-23-56-55'
TRAINING_MODELS = (
    (TRAINING_MODELS_T, 'OpenAI text model T'),
    # (TRAINING_MODELS_D, 'OpenAI text model D'),
    # (TRAINING_MODELS_C, 'OpenAI text model C'),
    # (TRAINING_MODELS_A1, 'OpenAI fine tuning text model A1'),
    # (TRAINING_MODELS_C1, 'OpenAI fine tuning text model C1'),
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
)