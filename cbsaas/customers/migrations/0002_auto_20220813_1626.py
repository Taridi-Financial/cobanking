# Generated by Django 3.2.13 on 2022-08-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='creation_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='tempcustomers',
            name='creation_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]