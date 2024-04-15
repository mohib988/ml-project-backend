from django.contrib import admin
from myapp import models

# Register your models here.
# admin.site.register(models.Anomaly)
# admin.site.register(models.NTN)
# # admin.site.register(models.POS)
# admin.site.register(models.MissingInvoice)
# admin.site.register(models.AnomalyInfo)

from django.contrib import admin
from . import models

from rest_framework.authtoken.admin import TokenProxy
admin.site.unregister(TokenProxy)
from allauth.account.admin import EmailAddress
admin.site.unregister(EmailAddress)

# Register your models here.
@admin.register(models.Anomaly)
class AnomalyAdmin(admin.ModelAdmin):
    # verbose_name = "Anomaly"
    # verbose_name_plural = "Anomalies"
    list_display = ['srb_invoice_id', 'pos_id', 'ntn', 'invoice_date', 'invoice_no','location','rate_value', 'sales_value', 'sales_tax', 'consumer_name', 'consumer_ntn', 'consumer_address', 'tariff_code', 'extra_info', 'pos_user', 'pos_pass', 'is_active', 'created_date_time', 'invoice_type', 'consider_for_annex', 'anomaly']
    list_filter = ['pos_id', 'ntn', 'invoice_date','location','anomaly'] 

@admin.register(models.NTN)
class NTNAdmin(admin.ModelAdmin):
    # verbose_name = "NTN"
    # verbose_name_plural = "NTNs"
    list_display = ['ntn', 'name']
    list_filter = ['ntn', 'name']

# admin.site.register(models.POS)

@admin.register(models.MissingInvoice)
class MissingInvoiceAdmin(admin.ModelAdmin):
    # verbose_name = "Missing Invoice"
    # verbose_name_plural = "Missing Invoices"
    list_display = ['ntn', 'pos_id', 'location', 'invoices', 'date']
    list_filter = ['ntn', 'pos_id', 'location', 'date']

@admin.register(models.AnomalyInfo)
class AnomalyInfoAdmin(admin.ModelAdmin):
    # verbose_name = "Anomaly Info"
    # verbose_name_plural = "Anomaly Info"
    list_display = ['id', 'description']

@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    # verbose_name = "Anomaly Info"
    # verbose_name_plural = "Anomaly Info"
    list_display = ['id', 'location']
    list_filter = ['id', 'location']
@admin.register(models.History)
class LocationAdmin(admin.ModelAdmin):
    # verbose_name = "Anomaly Info"
    # verbose_name_plural = "Anomaly Info"
    list_display = ['date', 'user','status']
    list_filter = ['date', 'user','status']
