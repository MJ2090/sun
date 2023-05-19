# Generated by Django 4.1.7 on 2023-05-19 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0004_alter_promptmodel_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialogue',
            name='completion_tokens',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dialogue',
            name='prompt_tokens',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dialogue',
            name='response_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dialogue',
            name='total_tokens',
            field=models.IntegerField(default=0),
        ),
    ]
