# Generated by Django 4.1.7 on 2023-05-18 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0002_alter_contact_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promptmodel',
            name='history',
            field=models.CharField(default='', max_length=1200),
        ),
    ]
