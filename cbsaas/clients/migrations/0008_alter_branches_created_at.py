# Generated by Django 3.2.13 on 2022-08-30 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_clients_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branches',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
