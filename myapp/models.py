from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator

# Create your models here.
class NTN(models.Model):
    ntn = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    # location = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f'{self.ntn} - {self.name}'
    
    class Meta:
        verbose_name = ("NTN")
        verbose_name_plural = ("NTNs")
    
class AnomalyInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    description=models.CharField(max_length=256)

    def __str__(self) -> str:
        return f'{self.id} - {self.description}'
    
    class Meta:
        verbose_name = ("Anomaly Info")
        verbose_name_plural = ("Anomaly Infos")

# class POS(models.Model):
#     pos = models.IntegerField()
#     ntn = models.ForeignKey(NTN, on_delete=models.PROTECT)
#     user = models.CharField(max_length=256, null=True)
#     password = models.CharField(max_length=256, null=True)

#     class Meta:
#         # This Meta class sets the composite primary key constraint
#         unique_together = ('pos', 'ntn')
class Location(models.Model):
    # id = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f'{self.id} - {self.location}'    

class Anomaly(models.Model):
    srb_invoice_id = models.CharField(primary_key=True, max_length=256)
    # pos = models.ForeignKey(POS, to_field="pos", on_delete=models.DO_NOTHING)
    pos_id = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    ntn = models.ForeignKey(NTN, on_delete=models.DO_NOTHING)
    invoice_date = models.DateTimeField()
    invoice_no = models.CharField(max_length=256, null=True)
    rate_value = models.FloatField(null=True)
    sales_value = models.FloatField(null=True)
    sales_tax = models.FloatField(null=True)
    consumer_name = models.CharField(max_length=256, null=True)
    # consumer_ntn = models.ForeignKey(NTN, on_delete=models.DO_NOTHING)
    consumer_ntn = models.CharField(null=True, max_length=256, blank=True)
    consumer_address = models.CharField(max_length=256, null=True)
    tariff_code = models.CharField(null=True, max_length=256, blank=True)
    extra_info = models.CharField(max_length=256, null=True)
    pos_user = models.CharField(max_length=256, null=True)
    pos_pass = models.CharField(max_length=256, null=True)
    is_active =models.BooleanField()
    created_date_time = models.DateTimeField()
    invoice_type = models.CharField(null=True, max_length=256, blank=True)
    consider_for_annex = models.IntegerField(null=True)
    anomaly = models.ForeignKey(AnomalyInfo, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return f'{self.srb_invoice_id} - {self.anomaly}'
    # anomaly = models.IntegerField(null=True)
    class Meta:
        verbose_name = ("Anomaly")
        verbose_name_plural = ("Anomalies")

class MissingInvoice(models.Model):
    ntn = models.ForeignKey(NTN, on_delete=models.DO_NOTHING)
    invoices = models.CharField(validators=[int_list_validator], max_length=10000)
    date = models.DateTimeField()
    pos_id = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name = ("Missing Invoice")
        verbose_name_plural = ("Missing Invoices")

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    query = models.CharField(max_length=256)
    status=models.BooleanField(default=False)
    class Meta:
        verbose_name = ("History")
        verbose_name_plural = ("Histories")
