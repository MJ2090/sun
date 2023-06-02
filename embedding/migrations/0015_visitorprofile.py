# Generated by Django 4.1.7 on 2023-06-02 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0014_embeddingmodel_reject_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100)),
                ('age', models.IntegerField(default=30)),
                ('gender', models.CharField(default='', max_length=50)),
                ('marriage', models.CharField(default='', max_length=50)),
                ('therapy_id', models.CharField(default='', max_length=20)),
                ('diagnosis', models.CharField(default='', max_length=50)),
                ('evidence', models.CharField(default='', max_length=1500)),
            ],
        ),
    ]
