from django.shortcuts import render
import pickle

from rest_framework import status
import pandas as pd
import datetime
import sqlite3
from urllib.parse import unquote
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from myapp import serializers, models
from rest_framework import generics
from rest_framework import filters
from ml_pipeline import missing_invoice, run_pipeline
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
import psycopg
from psycopg.rows import dict_row
# from django_filters import rest_framework as filters
# from . import filters

def time_to_sec(time):
    return time.hour * 3600 + time.minute * 60 + time.second

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, AllowAny])
@api_view(['GET'])
def get_user_role(request):
    # print(request.user.is_staff)
    # print(request.user.is_superuser)
    return Response({'is_admin': request.user.is_superuser, 'is_staff':request.user.is_staff})



class FilterView(generics.ListAPIView):
    # 
    # try:
    missing_data_serializer_class = serializers.MissingInvoiceSerializer
    missing_data_queryset = models.MissingInvoice.objects.all()

    anomaly_serializer_class = serializers.AnomalySerializer
    history_serializer_class = serializers.HistorySerializer
    history_data_queryset = models.History.objects.order_by("-date")[:20]
    anomaly_data_queryset = models.Anomaly.objects.all()

    anomaly_info_serializer_class = serializers.AnomalyInfoSerializer
    anomaly_info_data_queryset = models.AnomalyInfo.objects.all()

    ntn_serializer_class = serializers.NTNSerializer
    ntn_data_queryset = models.NTN.objects.all()

    location_serializer_class = serializers.LocationSerializer
    location_data_queryset = models.Location.objects.all()


    # pos_serializer_class = serializers.POSSerializer
    # pos_data_queryset = models.POS.objects.all()

    filter_backends = [filters.OrderingFilter]


    def get_queryset(self):
        # try:
        if any(param in self.request.query_params for param in ['missing_invoice_by_ntn', 'missing_invoice_by_date','missing_invoice_by_pos','missing_invoice_by_location', 'missing_invoice_by_date_range']):
            queryset = self.missing_data_queryset
        elif "ntn" in self.request.query_params:
            queryset = self.ntn_data_queryset
        elif "anomaly_info" in self.request.query_params:
            queryset = self.anomaly_info_data_queryset
        elif "location" in self.request.query_params:
            queryset = self.location_data_queryset
        elif "history" in self.request.query_params:
            queryset = self.history_data_queryset
        else:
            queryset = self.anomaly_data_queryset


        anomaly = self.request.query_params.get('anomaly')
        history = self.request.query_params.get('history')
        anomaly_by_pos = self.request.query_params.get('anomaly_by_pos')
        anomaly_by_ntn = self.request.query_params.get('anomaly_by_ntn')
        anomaly_by_srb_invoice_id = self.request.query_params.get('anomaly_by_srb_invoice_id')
        anomaly_by_date = self.request.query_params.get('anomaly_by_date')
        anomaly_by_location = self.request.query_params.get('anomaly_by_location')

        missing_invoice_by_date = self.request.query_params.get('missing_invoice_by_date')
        missing_invoice_by_ntn = self.request.query_params.get('missing_invoice_by_ntn')
        missing_invoice_by_pos = self.request.query_params.get('missing_invoice_by_pos')
        missing_invoice_by_location = self.request.query_params.get('missing_invoice_by_location')
        missing_invoice_by_date_range = self.request.query_params.get('missing_invoice_by_date_range')
        
        anomaly_info = self.request.query_params.get('anomaly_info')

        ntn = self.request.query_params.get('ntn')
        
        location = self.request.query_params.get('location')

        if anomaly is not None:
            
            anomaly_values = anomaly.split(',')
            if '10' not in anomaly_values:
                queryset = queryset.filter(anomaly__in=anomaly_values)
            
            else:
                queryset = queryset.exclude(anomaly=0)
               
        if anomaly_by_pos is not None :
            anomaly_by_pos_values = anomaly_by_pos.split(',')
            queryset = queryset.filter(pos_id__in=anomaly_by_pos_values)
        if anomaly_by_ntn is not None :
            anomaly_by_ntn_values = anomaly_by_ntn.split(',')
            queryset = queryset.filter(ntn__in=anomaly_by_ntn_values)
        if anomaly_by_date is not None :
            anomaly_by_date_range_values = anomaly_by_date.split(',')
            start_date_encoded = anomaly_by_date_range_values[0]
            end_date_encoded = anomaly_by_date_range_values[1]

            start_date = unquote(start_date_encoded)
            end_date = unquote(end_date_encoded)


            # Convert the decoded strings to datetime.datetime objects
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M')


            queryset = queryset.filter(
                created_date_time__range=(start_date,
            end_date )
            )
        if anomaly_by_srb_invoice_id is not None and isinstance(anomaly_by_srb_invoice_id, str):
            anomaly_by_srb_invoice_id_values = anomaly_by_srb_invoice_id.split(',')
            queryset = queryset.filter(srb_invoice_id__in=anomaly_by_srb_invoice_id_values)
        if anomaly_by_location is not None :
            anomaly_by_location_values = anomaly_by_location.split(',')
            queryset = queryset.filter(location__location__in=anomaly_by_location_values)

        
        if missing_invoice_by_date is not None :
            missing_invoice_by_date_values = missing_invoice_by_date.split(',')
            queryset = queryset.filter(date__in=missing_invoice_by_date_values)
        if missing_invoice_by_ntn is not None  :
            if missing_invoice_by_ntn == "all":
                queryset = queryset.all()
            else:
                missing_invoice_by_ntn_values = missing_invoice_by_ntn.split(',')
                queryset = queryset.filter(ntn__in=missing_invoice_by_ntn_values)
        if missing_invoice_by_pos is not None :
            missing_invoice_by_pos_values = missing_invoice_by_pos.split(',')
            queryset = queryset.filter(pos_id__in=missing_invoice_by_pos_values)
        if missing_invoice_by_location is not None :
            missing_invoice_by_location_values = missing_invoice_by_location.split(',')
            queryset = queryset.filter(location__location__in=missing_invoice_by_location_values)
        if missing_invoice_by_date_range is not None :
            missing_invoice_by_date_range_values = missing_invoice_by_date_range.split(',')
            start_date_encoded = missing_invoice_by_date_range_values[0]
            end_date_encoded = missing_invoice_by_date_range_values[1]

            start_date = unquote(start_date_encoded)
            end_date = unquote(end_date_encoded)


            # Convert the decoded strings to datetime.datetime objects
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M')


            queryset = queryset.filter(
                date__range=(start_date, end_date)
            )
        if anomaly_info is not None:
            if anomaly_info == "all":
                queryset = queryset.all()
            else:
                anomaly_info_values = anomaly_info.split(',')
                queryset = queryset.filter(id__in=anomaly_info_values)

        if history is not None:
            if history == "all":
                queryset = queryset.all()
        if ntn is not None:
            if ntn == "all":
                queryset = queryset.all()
            else:
                ntn_values = ntn.split(',')
                queryset = queryset.filter(ntn__in=ntn_values)

        if location is not None:
            if location == "all":
                queryset = queryset.all()
            else:
                location_values = location.split(',')
                queryset = queryset.filter(location__in=location_values)

        # if pos_in_ntn is not None:
        #     # print(ntn)
        #     # if ntn == "all":

        #         # print("all")
        #         # queryset = queryset.all()
        #     # else:
        #         # print(ntn)
        #     queryset = queryset.filter(ntn=pos_in_ntn)


        return queryset
    # except Exception as e:
        # return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_serializer_class(self):
        if any(param in self.request.query_params for param in ['missing_invoice_by_ntn', 'missing_invoice_by_date','missing_invoice_by_pos','missing_invoice_by_location', 'missing_invoice_by_date_range']):
            return self.missing_data_serializer_class
        elif "ntn" in self.request.query_params:
            return self.ntn_serializer_class
        elif "anomaly_info" in self.request.query_params:
            return self.anomaly_info_serializer_class
        elif "location" in self.request.query_params:
            return self.location_serializer_class
        elif "history" in self.request.query_params:
            return self.history_serializer_class
        # elif "pos_in_ntn" in self.request.query_params:
        #     return self.pos_serializer_class
        else:
            return self.anomaly_serializer_class

def connect_to_db(dbname, user, password, host, query,port):
    try:
        connection = psycopg.connect(dbname=dbname,
                                    user=user,
                                    password= password,
                                    host=host,
                                    port=port,
                                    row_factory=dict_row)
        # connection=sqlite3.connect("db.sqlite3")
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()
        # Example: Execute a SQL query
        cursor.execute(query)
        
        rows = cursor.fetchall()
        columns=[col[0] for col in cursor.description]

        cursor.close()
        connection.close()
        df=pd.DataFrame(rows,columns=columns)
        print(df)
        return df
    except Exception as e:
        print(e)
        return 

        
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(['POST'])
def add_location(request):
    try:
        print(request.data)
        dbname = request.data['dbname']
        username = request.data['username']
        host = request.data['host']
        password = request.data['password']
        query = request.data['query']
        port = request.data['port']
        df = connect_to_db(dbname, username, password, host, query)
        df.drop(columns=["id"],inplace=True)
        data=df.to_dict(orient='records')
        print(data)
        serializer = serializers.LocationSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(['POST'])
def add_anomaly(request):
    try:
        print(request.data)
        serializer = serializers.AnomalyInfoSerializer(data=request.data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_ntn(request):
    try:
        dbname = request.data['dbname']
        username = request.data['username']
        host = request.data['host']
        password = request.data['password']
        query = request.data['query']
        port = request.data['port']
        df = connect_to_db(dbname, username, password, host, query)
        data=df.to_dict(orient='records')
       
        serializer = serializers.NTNSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)    




@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(['POST'])
def missing_invoices(request):
    if request.method == "POST":
        # print(request.data)
        print(request.data)
        print(request.data)
        try:
            dbname = request.data['dbname']
            username = request.data['username']
            host = request.data['host']
            password = request.data['password']
            query = request.data['query']
            port = request.data['port']
            print(request.data)
            df = connect_to_db(dbname, username, password, host, query,port)

            df = df[['srb_invoice_id', 'pos_id',  'invoice_no', 'created_date_time',   'location', 'ntn']]
            df['created_date_time'] = df['created_date_time'].astype(str)
            
            # df["location"] = df["location_id"]
            # df["ntn"] = df["ntn_id"]
            # location_names = {location.pk: location.location for location in models.Location.objects.all()}
            # ntn_names = {ntn.pk: ntn.name for ntn in models.NTN.objects.all()}
            # df['name'] = df['ntn'].map(ntn_names)
            # df['location'] = df['location'].map(location_names)
            # # print(df2)
            result = missing_invoice.main(df)
            print(result)
            for i in result:
                i['location'] = models.Location.objects.get(location=i['location']).pk
              
        
            serializer = serializers.MissingInvoiceSerializer(data=result, many=True)
            if serializer.is_valid():
                print("valid")
                print(serializer.data)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                print("invalid")
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(['POST'])
def submit_data(request):
    if request.method == "POST":
        print(request.data)
        try:
            dbname = request.data['dbname']
            username = request.data['username']
            host = request.data['host']
            password = request.data['password']
            query = request.data['query']
            port = request.data['port']
            contamination = request.data['contamination']
            min_cluster = request.data['min_cluster']

            df = connect_to_db(dbname, username, password, host, query,port)
            df = df[['srb_invoice_id', 'pos_id', 'invoice_date', 'invoice_no', 'rate_value', 'sales_tax', 'consumer_name', 'consumer_ntn', 'consumer_address', 'tariff_code', 'extra_info', 
                         'pos_user', 'pos_pass', 'is_active', 'created_date_time', 'invoice_type', 'consider_for_annex',  'location', 'ntn',"name", 'sales_value']]
            df['invoice_date'] = df['invoice_date'].astype(str)
            df['created_date_time'] = df['created_date_time'].astype(str)
            
#             df["location"] = df["location_id"]
#             df["ntn"] = df["ntn_id"]
#             location_names = {location.pk: location.location for location in models.Location.objects.all()}
#             ntn_names = {ntn.pk: ntn.name for ntn in models.NTN.objects.all()}

# # Then, use the map function to lookup names based on primary keys
#             df['name'] = df['ntn'].map(ntn_names)
#             df['location'] = df['location'].map(location_names)
            df.rename(columns={'consider_for_annex': 'consider_for_Annex'}, inplace=True)
            df1 = df.to_dict(orient='records')
            
            serializer = serializers.AnomalySerializer(data=df1, many=True)
            
            if serializer.is_valid():
                prediction = run_pipeline.main(df,contamination=contamination,min_cluster=min_cluster)
                df['anomaly'] = prediction
                df.rename(columns={'consider_for_Annex': 'consider_for_annex'}, inplace=True)
                data = df.to_dict(orient='records')
                
                for record in data:
                    record['ntn'] = models.NTN.objects.get(ntn=record['ntn'])
                    record['location'] = models.Location.objects.get(location=record['location'])
                    record['anomaly'] = models.AnomalyInfo.objects.get(pk=record['anomaly'])
                    record['created_date_time'] = datetime.datetime.fromisoformat(record['created_date_time'])
                    del record['name']
                
                models.Anomaly.objects.bulk_create([models.Anomaly(**record) for record in data])
                
                history_data = {"user": request.user.pk, "query": request.data["query"], "status": True}
                history_serializer = serializers.HistorySerializer(data=history_data)
                
                if history_serializer.is_valid():
                    history_serializer.save()
                
                return Response(serializer.errors, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            history_data = {"user": request.user.pk, "query": request.data, "status": True}
            history_serializer = serializers.HistorySerializer(data=history_data)
            
            if history_serializer.is_valid():
                history_serializer.save()
            
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response("Method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)