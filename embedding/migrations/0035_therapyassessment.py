# Generated by Django 4.1.7 on 2023-06-12 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0034_rename_token_amount_request_quizrecord_token_request_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TherapyAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.IntegerField(default=0)),
                ('result', models.CharField(default='', max_length=30)),
                ('evidence', models.CharField(blank=True, default='', max_length=1500)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='embedding.visitorprofile')),
            ],
        ),
    ]
