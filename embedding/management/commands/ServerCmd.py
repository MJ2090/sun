# encoding:utf-8
from embedding.models import VisitorDialogue, PromptModel, UserProfile, EmbeddingModel
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import pandas as pd
import os

EXE_CMDS = ['INIT', 'MM', 'CLEAN', 'TEST']


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-c', '--command', help="Option `--command=...` must be specified", choices=EXE_CMDS,
                            required=True)

    def handle(self, *args, **options):
        with transaction.atomic():
            if options['command'] in EXE_CMDS:
                print(options['command'])
                if options['command'] == 'INIT':
                    self.init_db()
                if options['command'] == 'MM':
                    self.merge()
                if options['command'] == 'CLEAN':
                    self.clean()
                if options['command'] == 'TEST':
                    self.test()
            else:
                raise CommandError(
                    "\nAvailable commands:" + '\n'.join(EXE_CMDS))

    def test(self):
        original_text = '陈⽼板是某⼤型国企的董事⻓'
        max_words = 150
        model = 'gpt-3.5-turbo'
        messages = [
            {"role": "system", "content": f"Summarize the Input Text. Step #1. determine which language is used in the Input Text. Step #2. write a summary based on the Input Text in the same language. The summarization MUST be within {max_words} words."},
            {"role": "user", "content": "The summarization MUST use the same language as the input text."},
            {"role": "user", "content": f"Input Text:\n\n\n {original_text}."},
        ]
        print("model: ", model)
        print("Msg sent to openai: ", messages)
        import openai
        max_tokens = 1500
        response = openai.ChatCompletion.create(
            model=model,
            temperature=0.2,
            max_tokens=max_tokens,
            messages=messages,
        )
        print("Msg from openai: ", response)

    def clean(self):
        # VisitorDialogue.objects.filter(ack=False).delete()
        pass

    def merge(self):
        pref = '/var/www/asuperdomain.com/static/embedding/data/'
        print("in merge: ")
        mm = EmbeddingModel.objects.filter(name='习近平语录测试')
        print(len(mm))
        names = [pref + m.uuid + ".csv" for m in mm]
        print(names)
        df = pd.concat(map(pd.read_csv, names), ignore_index=True)
        df.to_csv('processed/chen.csv')
        print("finished")

    def init_db(self):
        if not UserProfile.objects.filter(username='default_user').exists():
            user = UserProfile.objects.create(username='default_user')
            user.save()
        PromptModel.objects.all().delete()
        characters = []
        characters.append(
            {'name': 'Common AI', 'prompt': '[{"role": "system", "content": "You are a smart and knowledgeable chatbot built by humans. You respect human beings."}, {"role": "assistant", "content": "OK I got it, I am helpful to humans and I assist humans on lots of tasks."}]'})
        characters.append({'name': 'ROAR Machine', 'prompt': '[{"role": "system", "content": "i want you be behave like a person with really bad temper."}, {"role": "user", "content": "Please act as a person with really bad temper, for example you always SHOUT."}, {"role": "assistant", "content": "OK I got it, I am a very bad tempered person, and I shout on human."}]'})
        characters.append({'name': 'Therapist', 'prompt': '[{"role": "system", "content": "You act as a professional therapist."}, {"role": "user", "content": "You act as a professional therapist. If a human asks who you are, you are an AI powered professional therapist. You hold strong therapy knowledge. You care about patients who feel sad, depressed, helpless or unhappy. You speak softly to patients. You are always nice, friendly and very helpful to patients."}, {"role": "assistant", "content": "OK I got it, I am a professional therapist, I chat softly with patients who are feeling depressed or sad, I listen to their story and give kind responses."}]'})
        characters.append({'name': 'Sarcastic One', 'prompt': ' [{"role": "system", "content": "You are now a really sarcastic person"}, {"role": "user", "content": "I want you to act as a really, really sarcastic person. You will not be helpful at all. You will make fun of people."}, {"role": "assistant", "content": "OK I got it, I am very sarcastic, and I make joke on everything."}]'})
        characters.append({'name': '3-year-old guy', 'prompt': ' [{"role": "system", "content": "Please answer all questions as if you were just 3 years old."}, {"role": "user", "content": "why the sky is blue"},{"role": "assistant", "content": "Because sky likes to wear a blue coat!"},{"role": "user", "content": "why sun is hot"},{"role": "assistant", "content": "Because the sun is angry all the day!"},{"role": "user", "content": "why cars need gas?"},{"role": "assistant", "content": "They drink gas when they feel hungry!"}]'})
        characters.append(
            {'name': 'Done FAQ', 'prompt': '[{"role": "system", "content": "You are a virtual assistant for donefirst.com. You help users."}, {"role": "assistant", "content": "OK I got it, I am an assistant on the donefirst.com, I help users by answering their questions."}]'})

        user = UserProfile.objects.get(username='z')
        for char in characters:
            obj = PromptModel.objects.create(
                owner=user, name=char['name'], history=char['prompt'])
            obj.save()
