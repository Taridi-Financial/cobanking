# Generated by Django 3.2.13 on 2022-06-29 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_rename_client_id_clients_client_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clients',
            old_name='client_uuid',
            new_name='client_ref',
        ),
    ]
