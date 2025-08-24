from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Accounts,AccountsUpload,capacity,capacityUpload,SalesRecords2,sales
from .serializer import AccountsSerializer,AccountsUploadSerializer,capacitySerializer,capacityUploadSerializer,SalesRecordsSerializer,salesSerializer
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
    queryset=capacity.objects.all()
    serializer_class=capacitySerializer


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
