# Generated by Django 4.1.7 on 2023-06-22 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embedding', '0037_fruitorder_order_id_fruitorder_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruitorder',
            name='pay_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]