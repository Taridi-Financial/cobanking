# Generated by Django 3.2.13 on 2022-06-30 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_rename_client_uuid_clients_client_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='identifying_number',
            field=models.CharField(max_length=100),
        ),
    ]
