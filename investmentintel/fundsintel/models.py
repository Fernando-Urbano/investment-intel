from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
from typing import Union, Literal
from datetime import datetime, date
import pandas as pd
import sqlite3

# Create your models here.
class InvestmentFund(models.Model):
    cnpj = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    fund_type = models.CharField(max_length=100, null=True)
    dt_registration = models.DateField(null=True)
    dt_establishment = models.DateField(null=True)
    dt_cancel = models.DateField(null=True)
    cd_cvm = models.IntegerField(null=True)
    situation = models.CharField(max_length=100, null=True)
    dt_situation = models.DateField(null=True)
    dt_exerc_start = models.DateField(null=True)
    dt_exerc_end = models.DateField(null=True)
    class_cvm = models.CharField(max_length=100, null=True)
    dt_class_cvm = models.DateField(null=True)
    dt_act_start = models.DateField(null=True)
    profitability = models.CharField(max_length=100, null=True)
    condominium_type = models.CharField(max_length=50, null=True)
    divided_in_quotas = models.BooleanField(null=True)
    exclusive = models.BooleanField(null=True)
    long_term_taxation = models.BooleanField(null=True)
    target_audience = models.CharField(max_length=50, null=True)
    ent_invest = models.BooleanField(null=True)
    performance_fee = models.FloatField(null=True)
    performance_fee_information = models.CharField(max_length=300, null=True)
    adm_fee = models.FloatField(null=True)
    adm_fee_information = models.CharField(max_length=300, null=True)
    net_equity = models.FloatField(null=True)
    dt_net_equity = models.DateField(null=True)
    director = models.CharField(max_length=150, null=True)
    adm_cnpj = models.CharField(max_length=30, null=True)
    adm = models.CharField(max_length=100, null=True)
    manager_pf_pj = models.CharField(max_length=10, null=True)
    manager_cpf_cnpj = models.CharField(max_length=30, null=True)
    manager = models.CharField(max_length=150, null=True)
    auditor_cnpj = models.CharField(max_length=30, null=True)
    auditor = models.CharField(max_length=150, null=True)
    custodian_cnpj = models.CharField(max_length=150, null=True)
    custodian = models.CharField(max_length=150, null=True)
    controler_cnpj = models.CharField(max_length=150, null=True)
    controler = models.CharField(max_length=150, null=True)
    authorized_to_invest_all_offshore = models.BooleanField(null=True)
    class_anbima = models.CharField(max_length=100, null=True)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.cnpj})"

    def save(self, *args, **kwargs):
        self.dt_updated = timezone.now()
        super().save(*args, **kwargs)

    @property
    def short_name(self):
        short_name = (
            self.name
            .replace("MULTIMERCADO", "MM")
            .replace("FUNDO DE INVESTIMENTO EM COTAS DE FUNDO DE INVESTIMENTO", "FICFI")
            .replace("FUNDO DE INVESTIMENTO EM COTAS DE FUNDOS DE INVESTIMENTO", "FICFI")
            .replace("FUNDO DE APLICACAO EM COTAS DE FUNDOS DE INVESTIMENTO", "FACFI")
            .replace("FUNDO DE INVESTIMENTO", "FI")
            .replace('REFERENCIADO', "REF")
            .replace("CURTO PRAZO", "CP")
            .replace("LONGO PRAZO", "LP")
            .replace("RENDA FIXA", "RF")
        )
        return short_name

    def get_data(
        self,
        data_type: Literal['quota', 'value', 'net_equity', 'raise_value', 'rescue_value'] = 'quota',
        start_dt_comptc: Union[datetime, date, None] = None,
        end_dt_comptc: Union[datetime, date, None] = None,
        data_path: str = 'fundsintel',
        normalize: bool = False
    ) -> dict:
        conn = sqlite3.connect(data_path + "\\" + "funds_info.db")
        query = f"""
            SELECT dt_comptc, {data_type}
            FROM daily_info
            WHERE cnpj = '{self.cnpj}'
        """
        if start_dt_comptc:
            start_dt_comptc = start_dt_comptc.strftime("%Y-%m-%d")
            query += f" AND dt_comptc >= {start_dt_comptc}"
        if end_dt_comptc:
            end_dt_comptc = end_dt_comptc.strftime("%Y-%m-%d")
            query += f" AND dt_comptc <= {end_dt_comptc}"
        query += " ORDER BY dt_comptc"
        fund_data = pd.read_sql(query, conn)
        if normalize:
            fund_data[data_type] = fund_data[data_type] / fund_data[data_type][0]
        fund_data.set_index('dt_comptc', inplace=True)
        return fund_data[data_type].to_dict()

    def serialize(self):
        return {
            "id": self.id,
            "cnpj": self.cnpj,
            "name": self.name,
            "short_name": self.short_name,
            "class_cvm": self.class_cvm,
            "class_anbima": self.class_anbima,
        }
    

class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    users_following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followed_by')
    funds_watchlist = models.ManyToManyField('InvestmentFund', blank=True, related_name='watched_by')
    funds_liked = models.ManyToManyField('InvestmentFund', blank=True, related_name='liked_by')

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'auth_user'

    def __str__(self):
        return self.username

    def like_fund(self, fund):
        self.funds_liked.add(fund)
        
    def watch_fund(self, fund):
        self.funds_watchlist.add(fund)

    @property
    def number_followers(self):
        return len(self.followed_by.all())

    @property
    def number_following(self):
        return len(self.users_following.all())

    @property
    def number_post_watching(self):
        return len(self.watchlist)