# Generated by Django 4.1.7 on 2023-05-02 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0009_dialogue'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialogue',
            name='source',
            field=models.CharField(default='chat', max_length=20),
        ),
    ]
