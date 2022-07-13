# Generated by Django 3.2.13 on 2022-06-25 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CINRegistry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('cin', models.CharField(blank=True, max_length=300, null=True)),
                ('identifying_number', models.CharField(blank=True, max_length=300, null=True)),
                ('owner_type', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.clients')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]