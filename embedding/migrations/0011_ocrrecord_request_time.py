# Generated by Django 4.1.7 on 2023-05-25 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0010_quizrecord_request_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocrrecord',
            name='request_time',
            field=models.IntegerField(default=0),
        ),
    ]