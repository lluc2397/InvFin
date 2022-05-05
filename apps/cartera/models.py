from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    OneToOneField,
    ForeignKey,
    TextField,
    DateTimeField,
    BooleanField,
    PositiveIntegerField,
    IntegerField,
    ManyToManyField,
    JSONField,
    DateField,
    DecimalField
)
import json
from decimal import Decimal
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.general.utils import ChartSerializer
from apps.empresas.models import (
    Currency,
    Company,
    )

from apps.etfs.models import (
    Etf)

from django.contrib.auth import get_user_model
User = get_user_model()    


class Asset(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    content_type = ForeignKey(ContentType, on_delete=SET_NULL, null=True)
    object_id = PositiveIntegerField()
    object = GenericForeignKey("content_type", "object_id")
    is_stock = BooleanField(default=False)
    is_etf = BooleanField(default=False)
    is_crypto = BooleanField(default=False)

    class Meta:        
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
        db_table = "cartera_assets"

    def __str__(self):       
        return str(self.name)
    
    @property
    def amount_invested(self):
        return sum(move.movement_cost for move in PositionMovement.objects.filter(asset_related = self))


class PositionMovement(Model):
    MOVE = ((1, "Compra"), (2, "Venta"))

    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    move_type = IntegerField(choices=MOVE, null=True, blank=True)
    asset_related = ForeignKey(Asset, null=True, blank=True ,on_delete=SET_NULL, related_name='movements')
    price = DecimalField ("Precio", max_digits=100, decimal_places=2, default=0)
    date = DateField("Fecha del movimiento", null=True, blank=True)
    quantity = IntegerField("Cantidad", default=0)
    currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)
    observacion = TextField("Observaciones", default='')
    fee = DecimalField ("Comisión", max_digits=100, decimal_places=2, default=0)

    class Meta:        
        ordering = ['date']
        verbose_name = "Position movement"
        verbose_name_plural = "Position movements"
        db_table = "cartera_movements"

    def __str__(self):
        return str(self.id)
    
    @property
    def movement_cost(self):
        total = (self.price * self.quantity) - self.fee
        if self.move_type == 2:
            total = total * (-1)
        return total


class CashflowMovementCategory(Model):
    name = CharField("Nombre",max_length=1000)
    date_created = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cashflow category"
        verbose_name_plural = "Cashflow categories"
        db_table = "cartera_cashflow_category"
    
    def __str__(self):
        return self.name


class CashflowMovement(Model):
    user = ForeignKey(User,  on_delete=SET_NULL, null=True, blank=True)
    name = CharField("Nombre",max_length=1000)
    amount = DecimalField ("Monto", max_digits=100, decimal_places=2, default=0)
    description = TextField("Descripción", default='')
    date = DateField("Fecha del movimiento", null=True, blank=True)
    currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)
    is_recurrent = BooleanField(default=False)
    category = ForeignKey(CashflowMovementCategory,  on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True      
        ordering = ['date']
    
    def __str__(self):
        return self.name


class Income(CashflowMovement):
    class Meta:
        verbose_name = "Income"
        verbose_name_plural = "Incomes"
        db_table = "cartera_income"


class Spend(CashflowMovement):
    class Meta:
        verbose_name = "Spend"
        verbose_name_plural = "Spends"
        db_table = "cartera_spend"


class FinancialObjectif(Model):
    user = ForeignKey(User, 
        on_delete=SET_NULL, 
        null=True, blank=True
    )
    name = CharField("Nombre",max_length=1000)
    date_created = DateTimeField(auto_now_add=True)
    date_to_achieve = DateTimeField(null=True, blank=True)
    date_achived = DateTimeField(null=True, blank=True)
    observation = TextField("Observaciones", default='')
    accomplished = BooleanField(default=False)
    abandoned = BooleanField(default=False)
    percentage = DecimalField ("Porcentaje", 
        max_digits=100, decimal_places=2, 
        default=0
    )
    amount = DecimalField ("Monto", 
        max_digits=100, decimal_places=2, 
        default=0
    )
    is_rule = BooleanField(default=False)
    rule_ends = BooleanField(default=False)
    requirement = JSONField(default=dict)
    start_date = DateTimeField(null=True, blank=True)
    end_date = DateTimeField(null=True, blank=True)

    class Meta:        
        ordering = ['date_created']
        verbose_name = "Objetivo financiero"
        verbose_name_plural = "Objetivo financieros"
        db_table = "cartera_objectives"


class Patrimonio(Model, ChartSerializer):
    user = OneToOneField(User, 
        on_delete=SET_NULL, 
        null=True, blank=True, 
        related_name='user_patrimoine'
    )
    assets = ManyToManyField(Asset, blank=True)
    objectives = ManyToManyField(FinancialObjectif, blank=True)
    default_currency = ForeignKey(Currency, 
        on_delete=SET_NULL, 
        null=True, blank=True, 
        default='USD'
    )

    class Meta:        
        verbose_name = "Patrimonio"
        verbose_name_plural = "Patrimonios"
        db_table = "cartera_patrimoine"

    def __str__(self):
        return self.user.username

    @property
    def patrimoine(self):
        user = self.user
        incomes = list(Income.objects.filter(user = user))
        spends = list(Spend.objects.filter(user = user))
        income_earned = sum(move.amount for move in incomes) 
        income_spend = sum(move.amount for move in spends)
        income_saved = income_earned - income_spend
        income_invested = sum(move.amount_invested for move in Asset.objects.filter(user = user))

        data = {
            'income_earned':str(income_earned),
            'income_spend':str(income_spend),
            'income_saved':str(income_saved),
            'income_invested':str(income_invested),
            'incomes_and_spends':incomes+ spends,
        }
        return data
    
    # comparaison_dict = {
    #         'label': field['title'],
    #         'data': field['values'],
    #         'backgroundColor': '',
    #             'borderColor': '',
            
    #         'yAxisID':"right",
    #         'order': 0,
    #         'type': chart_type
    # }
    
    # def serial():
    #     inc_json = {
    #         'labels': [data.date for data in inc],
    #         'fields': [
    #             {'title':'Ingresos',
    #             'url':"#!",
    #             'percent': 'false',
    #             'short': 'false',
    #             'values' : [data.revenue for data in inc]},]}

    @property
    def empresass_en_cartera (self):
        return [empresa.object for empresa in self.assets.filter(is_stock=True)]
    
    @property
    def porcentaje_empresas_en_cartera (self):
        return sum(Decimal(item.percentage_capital_invested) for item in self.empresas_en_cartera)


    @property
    def gastos_totales(self):
        total = sum(Decimal(item.amount) for item in Spend.objects.filter(user = self.user))
        if total == None:
            total = 0
        return total
    
    @property
    def ingresos_totales (self):
        total = sum(Decimal(item.amount) for item in Income.objects.filter(user = self.user))
        if total == None:
            total = 0
        return total
    
    @property
    def cantidad_total_invertida(self):
        total_invertido = sum(item.amount_invested for item in self.assets.all())
        if total_invertido == None:
            total_invertido = 0
        return total_invertido
    
    @property
    def ahorros_totales(self):
        return self.ingresos_totales - self.gastos_totales - self.cantidad_total_invertida
    
    @property
    def porcentaje_ahorros_totales (self):        
        return (((self.ahorros_totales) / self.ingresos_totales) * 100) if self.ingresos_totales != 0 else 0   

    
    @property
    def porcentaje_cantidad_invertida(self):
        return ((self.cantidad_total_invertida / self.ingresos_totales) * 100) if self.ingresos_totales != 0 else 0

    @property
    def porcentaje_gastos_totales(self):
        return ((self.gastos_totales / self.ingresos_totales) * 100) if self.ingresos_totales != 0 else 0

