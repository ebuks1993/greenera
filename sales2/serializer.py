from rest_framework import serializers
from django.db import transaction
from django.db.models import Count
from .models import Accounts,capacity,sales , SalesRecords,AccountsUpload,capacityUpload
import requests


class AccountsSerializer (serializers.ModelSerializer):
    class Meta:
        model=Accounts
        fields='__all__'


class capacitySerializer (serializers.ModelSerializer):
    class Meta:
        model=capacity
        fields='__all__'


class salesSerializer (serializers.ModelSerializer):
    class Meta:
        model=sales
        fields='__all__'


class SalesRecordsSerializer (serializers.ModelSerializer):
    class Meta:
        model=SalesRecords
        fields='__all__'

class AccountsUploadSerializer (serializers.ModelSerializer):
    class Meta:
        model=AccountsUpload
        fields='__all__'

class capacityUploadSerializer (serializers.ModelSerializer):
    class Meta:
        model=capacityUpload
        fields='__all__'