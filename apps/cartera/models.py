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


class Patrimonio(Model):
    usuario = OneToOneField(User, on_delete=SET_NULL, null=True, blank=True)
    assets = ManyToManyField('cartera.Asset', blank=True)
    liabilities = ManyToManyField('cartera.Liability', blank=True)
    cashflow = ManyToManyField('cartera.CashflowMovement', blank=True)
    default_currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)

    class Meta:        
        verbose_name = "Patrimonio"
        verbose_name_plural = "Patrimonios"

    def __str__(self):
        return self.usuario.username
    
    @property
    def empresas_en_cartera (self):
        empresas = []
        for empresa in self.cartera.all():
            if empresa.asset is not None and empresa.asset.empresa is not None:            
                empresas.append(empresa)
        return empresas
    
    @property
    def porcentaje_empresas_en_cartera (self):
        return sum(Decimal(item.percentage_capital_invested) for item in self.empresas_en_cartera)
    
    
    @property
    def porcentaje_etfs_en_cartera (self):
        etfs = []
        for etf in self.cartera.all():
            if etf.asset is not None and etf.asset.etf is not None:
                etfs.append(etf)
        return sum(Decimal(item.percentage_capital_invested) for item in etfs)


    @property
    def gastos_totales(self):
        total = sum(Decimal(item.amount) for item in self.cashflow.filter(move_type = 2))
        if total == None:
            total = 0
        return total
    
    @property
    def ingresos_totales (self):
        total = sum(Decimal(item.amount) for item in self.cashflow.filter(move_type = 1))
        if total == None:
            total = 0
        return total
    
    @property
    def cantidad_total_invertida(self):
        total_invertido = sum((item.price) * item.quantity for item in self.cartera.all())
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


class Liability(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    name = CharField(max_length=10000, null=True, blank=True)
    observation = TextField("Observaciones", default='')
    amount = DecimalField ("Cantidad", max_digits=100, decimal_places=2, default=0)


class Asset(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    name = CharField(max_length=10000, null=True, blank=True)
    content_type = ForeignKey(ContentType, on_delete=SET_NULL, null=True)
    object_id = PositiveIntegerField()
    object = GenericForeignKey("content_type", "object_id")
    is_stock = BooleanField(default=False)
    is_etf = BooleanField(default=False)
    is_crypto = BooleanField(default=False)
    average_price = DecimalField ("Valor", max_digits=100, decimal_places=2, default=0)
    total_quantity = IntegerField("Cantidad", default=0)
    total_fees = DecimalField ("Comisiones totales", max_digits=100, decimal_places=2, default=0)
    sold_out = BooleanField(default=False)

    class Meta:        
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.content_type
        return super().save(*args, **kwargs)

    def __str__(self):       
        return str(self.name)
    
    @property
    def last_income_statement(self):
        info = None
        if self.asset.empresa is not None:
            info = self.asset.empresa.income_statement_set.latest('date')
        return info
    
    @property
    def last_balance_statement(self):
        info = None
        if self.asset.empresa is not None:
            info = self.asset.empresa.balance_sheet_set.latest('date')
        return info
    
    @property
    def last_cashflow_statement(self):
        info = None
        if self.asset.empresa is not None:
            info = self.asset.empresa.cashflow_statement_set.latest('date')
        return info
    
    @property
    def last_rentability(self):
        info = None
        if self.asset.empresa is not None:
            info = self.asset.empresa.rentability_ratio_set.latest('date')
        return info
    
    @property
    def last_per_share_value(self):
        info = None
        if self.asset.empresa is not None:
            info = self.asset.empresa.per_share_value_set.latest('date')
        return info
    
    @property
    def last_growth(self):
        info = None
        if self.asset.empresa is not None:
            info = self.asset.empresa.company_growth_set.latest('date')
        return info
    
    @property
    def capital_invested(self):
        return self.price * self.quantity
    
    @property
    def percentage_capital_invested(self):
        total_invertido = self.user.patrimonio.cantidad_total_invertida
        total_position = self.quantity * self.price

        return ((total_position / total_invertido) * 100) if total_invertido !=0 else 0


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

    def __str__(self):
        return str(self.id)
    
    @property
    def total_price(self):
        return self.price * self.quantity


class CashflowMovement(Model):
    MOVE = ((1, "Ingreso"), (2, "Gasto"))

    user = ForeignKey(User,  on_delete=SET_NULL, null=True, blank=True)
    name = CharField("Nombre",max_length=1000)
    amount = DecimalField ("Monto", max_digits=100, decimal_places=2, default=0)
    description = TextField("Descripción", default='')
    date = DateField("Fecha del movimiento", null=True, blank=True)
    currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)
    is_recurrent = BooleanField(default=False)
    move_type = IntegerField(choices=MOVE, null=True, blank=True)

    class Meta:        
        ordering = ['date']
        verbose_name = "Cashflow movement"
        verbose_name_plural = "Cashflow movements"
    
    def __str__(self):
        return self.name


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
