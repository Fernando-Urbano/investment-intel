# Generated by Django 4.1.4 on 2023-06-27 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('fund_type', models.CharField(max_length=100, null=True)),
                ('dt_registration', models.DateField(null=True)),
                ('dt_establishment', models.DateField(null=True)),
                ('dt_cancel', models.DateField(null=True)),
                ('cd_cvm', models.IntegerField(null=True)),
                ('situation', models.CharField(max_length=100, null=True)),
                ('dt_situation', models.DateField(null=True)),
                ('dt_exerc_start', models.DateField(null=True)),
                ('dt_exerc_end', models.DateField(null=True)),
                ('class_cvm', models.CharField(max_length=100, null=True)),
                ('dt_class_cvm', models.DateField(null=True)),
                ('dt_act_start', models.DateField(null=True)),
                ('profitability', models.CharField(max_length=100, null=True)),
                ('condominium_type', models.CharField(max_length=50, null=True)),
                ('divided_in_quotas', models.BooleanField(null=True)),
                ('exclusive', models.BooleanField(null=True)),
                ('long_term_taxation', models.BooleanField(null=True)),
                ('target_audience', models.CharField(max_length=50, null=True)),
                ('ent_invest', models.BooleanField(null=True)),
                ('performance_fee', models.FloatField(null=True)),
                ('information_performance_fee', models.CharField(max_length=300, null=True)),
                ('adm_fee', models.FloatField(null=True)),
                ('information_adm_fee', models.CharField(max_length=300, null=True)),
                ('net_equity', models.FloatField(null=True)),
                ('dt_net_equity', models.DateField(null=True)),
                ('director', models.CharField(max_length=150, null=True)),
                ('cnpj_adm', models.CharField(max_length=30, null=True)),
                ('adm', models.CharField(max_length=100, null=True)),
                ('pf_pj_manager', models.CharField(max_length=10, null=True)),
                ('cpf_cnpj_manager', models.CharField(max_length=30, null=True)),
                ('manager', models.CharField(max_length=150, null=True)),
                ('cnpj_auditor', models.CharField(max_length=30, null=True)),
                ('auditor', models.CharField(max_length=150, null=True)),
                ('cnpj_custodian', models.CharField(max_length=150, null=True)),
                ('custodian', models.CharField(max_length=150, null=True)),
                ('cnpj_controler', models.CharField(max_length=150, null=True)),
                ('controler', models.CharField(max_length=150, null=True)),
                ('authorized_to_invest_all_offshore', models.BooleanField(null=True)),
                ('class_anbima', models.CharField(max_length=100, null=True)),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('dt_update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
