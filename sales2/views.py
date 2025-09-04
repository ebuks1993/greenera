from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from django.db.models.functions import Coalesce
from django.db.models import OuterRef, Subquery, Value, IntegerField

from .models import Accounts,AccountsUpload,capacity,capacityUpload,SalesRecords2,sales
from .serializer import AccountsSerializer,AccountsUploadSerializer,capacitySerializer,capacityUploadSerializer,SalesRecordsSerializer,salesSerializer,AccountsSerializer2
# from django.db.models import Value,F
# from django.db.models import Count, Sum, F, Window, Avg, Max, Min 
# from django.db.models.functions import TruncDate



class AccountsView(ModelViewSet):
    queryset=Accounts.objects.all()
    serializer_class=AccountsSerializer

class AccountsUploadView(ModelViewSet):
    queryset=AccountsUpload.objects.all()
    serializer_class=AccountsUploadSerializer

class capacityView(ModelViewSet):
    # queryset=capacity.objects.all()
    def get_queryset(self):
        cred_lim=Accounts.objects.filter(Allias=OuterRef('Allias')).values("Credit_limit")[:1]
        # cur_sales=SalesRecords2.objects.filter(Allias=OuterRef('Allias'),month='8',year='2025')
        return capacity.objects.annotate(
            credit_cap=Coalesce(
                Subquery(cred_lim, output_field=IntegerField()),  # 👈 fix here
                Value(0),
                output_field=IntegerField()
            )
        )
        
    serializer_class=capacitySerializer

class accountview2(ModelViewSet):
    def get_queryset(self):
        debt=capacity.objects.filter(Allias=OuterRef("Allias")).values("Balance")[:1]
        sales= capacity.objects.filter(Allias=OuterRef("Allias")).values("Sales")[:1]

        qd=Accounts.objects.all().annotate(debt=Coalesce(Subquery(debt,output_field=IntegerField()),Value(0),output_field=IntegerField())).annotate(sales=Coalesce(Subquery(sales,output_field=IntegerField()),Value(0),output_field=IntegerField()))

        return qd
    
    serializer_class=AccountsSerializer2






class capacityUploadView(ModelViewSet):
    queryset=capacityUpload.objects.all()
    serializer_class=capacityUploadSerializer

class SalesRecordsView(ModelViewSet):
    queryset=SalesRecords2.objects.all()
    serializer_class=SalesRecordsSerializer

class salesView(ModelViewSet):
    queryset=sales.objects.all()
    serializer_class=salesSerializer
# Create your views here.
