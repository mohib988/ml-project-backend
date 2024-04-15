from myapp import models
from rest_framework import serializers

class NTNSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.NTN
        fields = '__all__' 

# class POSSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model=models.POS
#         fields = '__all__'

class AnomalySerializer(serializers.ModelSerializer):
    description = serializers.CharField(source='anomaly.description', read_only=True)
    location = serializers.CharField(source='location.location', read_only=True)
    # location = serializers.CharField(source='ntn.location', read_only=True)

    class Meta:
        model=models.Anomaly
        # fields = '__all__' 
        fields = ['srb_invoice_id', 'pos_id', 'ntn', 'location','invoice_date', 'invoice_no', 'rate_value', 'sales_value', 'sales_tax', 'consumer_name', 'consumer_ntn', 'consumer_address', 'tariff_code', 'extra_info', 'pos_user', 'pos_pass', 'is_active', 'created_date_time', 'invoice_type', 'consider_for_annex', 'anomaly', 'description']


class MissingInvoiceSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.location', read_only=True)

    class Meta:
        model=models.MissingInvoice
        fields = ['location', 'location_name', 'ntn', 'pos_id', 'invoices', 'date']

class AnomalyInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.AnomalyInfo
        fields = '__all__' 


class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.Location
        fields = '__all__' 
class HistorySerializer(serializers.ModelSerializer):
    username=serializers.CharField(source="user.username",read_only=True)
    class Meta:
        model=models.History
        fields = '__all__' 