# Generated by Django 4.1.7 on 2023-06-06 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0021_embeddingdocument_summarization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embeddingdocument',
            name='summarization',
            field=models.CharField(default='Processing', max_length=5000),
        ),
    ]
