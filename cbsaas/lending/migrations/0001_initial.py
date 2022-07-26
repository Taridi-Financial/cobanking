# Generated by Django 3.2.13 on 2022-07-07 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0005_alter_branches_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanProductCharges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('charge_frequency', models.CharField(max_length=100)),
                ('charge_moment', models.CharField(max_length=100)),
                ('charge_value_type', models.CharField(max_length=100)),
                ('charge_value', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MobileLoans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('loan_type_code', models.CharField(max_length=100)),
                ('loan_ref', models.CharField(blank=True, max_length=100, null=True)),
                ('applied_amount', models.CharField(max_length=100)),
                ('amount_disbursed', models.CharField(default=0, max_length=100)),
                ('loan_status', models.CharField(max_length=100)),
                ('applied_by', models.CharField(max_length=100)),
                ('approved_by', models.CharField(blank=True, max_length=100, null=True)),
                ('date_applied', models.CharField(max_length=100)),
                ('date_disbursed', models.DateField(blank=True, null=True)),
                ('date_cleared', models.DateField(blank=True, null=True)),
                ('loan_wallet_ref', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MobileLoansOperations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='LoanProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('loan_code', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=100)),
                ('lower_limit', models.CharField(max_length=100)),
                ('upper_limit', models.CharField(max_length=100)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.clients')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]