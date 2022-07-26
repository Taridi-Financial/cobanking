# Generated by Django 3.2.13 on 2022-07-12 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0003_auto_20220701_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='ledgerwalletrecords',
            name='related_source',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='ledgerwalletrecords',
            name='related_source_ref',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='loanwalletrecords',
            name='related_source',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='loanwalletrecords',
            name='related_source_ref',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='normalwalletrecords',
            name='related_source',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='normalwalletrecords',
            name='related_source_ref',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]