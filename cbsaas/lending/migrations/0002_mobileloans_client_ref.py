# Generated by Django 3.2.13 on 2022-07-12 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lending', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobileloans',
            name='client_ref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
