# Generated by Django 4.1.7 on 2023-06-12 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0033_quizrecord_token_amount_request_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizrecord',
            old_name='token_amount_request',
            new_name='token_request',
        ),
        migrations.RenameField(
            model_name='quizrecord',
            old_name='token_amount_response',
            new_name='token_response',
        ),
    ]
