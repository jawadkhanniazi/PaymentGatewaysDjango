# Generated by Django 4.1.4 on 2023-02-06 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_orderdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='jsonResonse',
            field=models.TextField(default='google.com'),
            preserve_default=False,
        ),
    ]
