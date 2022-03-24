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
    FloatField,
    DateField,
    DecimalField
)
import json
from decimal import Decimal
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
        moves = PositionMovement.objects.filter(asset_related = self)
        return sum(move.movement_cost for move in moves)


class PositionMovement(Model):
    MOVE = ((1, "Compra"), (2, "Venta"))

    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    move_type = IntegerField(choices=MOVE, null=True, blank=True)
    asset_related = ForeignKey(Asset, null=True, blank=True ,on_delete=SET_NULL)
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
    

class CashflowMovement(Model):
    user = ForeignKey(User,  on_delete=SET_NULL, null=True, blank=True)
    name = CharField("Nombre",max_length=1000)
    amount = DecimalField ("Monto", max_digits=100, decimal_places=2, default=0)
    description = TextField("Descripción", default='')
    date = DateField("Fecha del movimiento", null=True, blank=True)
    currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)
    is_recurrent = BooleanField(default=False)

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
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    name = CharField(max_length=50000)
    date_created = DateTimeField(auto_now_add=True)
    date_to_achieve = DateTimeField(null=True, blank=True)
    date_achived = DateTimeField(null=True, blank=True)
    observation = TextField("Observaciones", default='')
    accomplished = BooleanField(default=False)
    abandoned = BooleanField(default=False)
    percentage = DecimalField ("Porcentaje", max_digits=100, decimal_places=2, default=0)
    amount = DecimalField ("Monto", max_digits=100, decimal_places=2, default=0)

    class Meta:        
        ordering = ['date_created']
        verbose_name = "Objetivo financiero"
        verbose_name_plural = "Objetivo financieros"
        db_table = "cartera_objectives"


class Patrimonio(Model):
    user = OneToOneField(User, on_delete=SET_NULL, null=True, blank=True)
    assets = ManyToManyField(Asset, blank=True)
    objectives = ManyToManyField(FinancialObjectif, blank=True)
    default_currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)

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

