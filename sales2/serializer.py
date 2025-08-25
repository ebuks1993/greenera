from rest_framework import serializers
from django.db import transaction
from django.db.models import Count
from .models import Accounts,capacity,sales , SalesRecords2,AccountsUpload,capacityUpload
from django.db.models import OuterRef, Subquery
import requests


class AccountsSerializer (serializers.ModelSerializer):
    class Meta:
        model=Accounts
        fields='__all__'


# cred_lim=Accounts.objects.filter(Name=OuterRef('Name')).values("Credit_limit")[:1]
# accounts=capacity.objects.annotate(
#     credit_cap=Subquery(cred_lim)
# )

class capacitySerializer (serializers.ModelSerializer):
    credit_cap=serializers.IntegerField(read_only=True)
    # cred_cap = serializers.IntegerField(read_only=True)
    # cred_cap = serializers.SerializerMethodField()
    class Meta:
        model=capacity
        fields=['id','Name','Sales','collection','Balance','credit_cap']

    # def get_cred_cap(self, obj):
    #     return getattr(obj, "cred_cap", None)


class salesSerializer (serializers.ModelSerializer):
    class Meta:
        model=sales
        fields='__all__'


class SalesRecordsSerializer (serializers.ModelSerializer):
    class Meta:
        model=SalesRecords2
        fields='__all__'

class AccountsUploadSerializer (serializers.ModelSerializer):
    class Meta:
        model=AccountsUpload
        fields='__all__'

class capacityUploadSerializer (serializers.ModelSerializer):
    class Meta:
        model=capacityUpload
        fields='__all__'