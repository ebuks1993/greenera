from rest_framework import serializers
from django.db import transaction
from django.db.models import Count
from .models import Accounts,capacity,sales , SalesRecords2,AccountsUpload,capacityUpload,salesStructure
from django.db.models import OuterRef, Subquery
import requests


class AccountsSerializer (serializers.ModelSerializer):
    class Meta:
        model=Accounts
        fields='__all__'


class AccountsSerializer2 (serializers.ModelSerializer): ## conjunction with capacity 
    debt=serializers.FloatField(read_only=True)
    sales=serializers.FloatField(read_only=True)
    # msales=serializers.FloatField(read_only=True)
    region=serializers.SerializerMethodField()
    channel=serializers.SerializerMethodField()
    overdue=serializers.SerializerMethodField()
    overlimit=serializers.SerializerMethodField()
    emails=serializers.SerializerMethodField()
    class Meta:
        model=Accounts
        fields=['Name','Allias','Parent','Credit_limit','debt','sales','region',"channel",'overdue','overlimit','emails']

    def get_region(self, acct:Accounts):
        ak=['EMA','EMDE','EMDM']
        ag=['WMA','WMDE','WMDM']
        an=['NMA','NMDE','NMDM']
        la=['LMA','LMDE','LMDM']
        ca=['CSR','CHT']
        if any(x in acct.Name.upper() for x in ak):
            return "EAST"
        if any(x in acct.Name.upper() for x in ag):
            return "WEST"
        if any(x in acct.Name.upper() for x in an):
            return "NORTH"
        if any(x in acct.Name.upper() for x in la):
            return "LAGOS"
        if any(x in acct.Name.upper() for x in ca):
            return "CONSUMER"
        else:
            return "OTHERS"

    def get_channel(self,acct:Accounts):
        ak=['MDE','CSR',]
        if any(x in acct.Name for x in ak):
            return "REP"
        elif 'WHOLESALER' in acct.Parent.upper():
            return "WHOLESALER"
        
        elif 'MINOR SALES GROUP' in acct.Parent.upper():
            return "SUB-DISTRIBUTOR"
        elif 'PERFORMING' in acct.Parent.upper():
            return "BLOCKED ACCOUNT"
        else:
            return "OTHERS"


    def get_overdue (self,acct:Accounts):
        try:
            if int(acct.debt) > (acct.sales):
                a=int(acct.debt) - int(acct.sales)
                return a
            else:
                return 0
        except:
            return -1
    
    def get_overlimit (self,acct:Accounts):
        try:
            if int(acct.debt) > (acct.Credit_limit):
                a=int(acct.debt) - int(acct.Credit_limit)
                return a
            else:
                return 0
        except:
            return -1
    
    # def get_emails(self,acct:Accounts):
    #     region1 = self.get_region(acct)
         
    #     if not hasattr (self,'_region_mapping'):
    #          self._region_mapping = {
    #              r.region.upper(): r.email
    #              for r in salesStructure.objects.all()
    #          }
    #     return self._region_mapping.get(region1.upper(), "default@example.com")

    def get_emails(self, acct):
        region = self.get_region(acct)

        # Cache mapping for performance
        if not hasattr(self, "_region_mapping"):
            self._region_mapping = {}
            qs = salesStructure.objects.values("region", "email")
            for row in qs:
                reg = row["region"].upper()
                if reg not in self._region_mapping:
                    self._region_mapping[reg] = []
                self._region_mapping[reg].append(row["email"])

        # Get all emails for region as comma-separated string
        emails = self._region_mapping.get(region.upper(), [])
        return ", ".join(emails) if emails else "no-email@example.com"        






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
        fields=['id','Name','Sales','collection','Balance','credit_cap','Allias']

    
 
        

    # def get_cred_cap(self, obj):
    #     return getattr(obj, "cred_cap", None)


class salesSerializer (serializers.ModelSerializer):
    class Meta:
        model=sales
        fields='__all__'


class SalesRecordsSerializer (serializers.ModelSerializer):
    region=serializers.SerializerMethodField()
    emails=serializers.SerializerMethodField()
    class Meta:
        model=SalesRecords2
        fields=['id','VoucherNum','Date','units','ctns','rate','Amount','temp_region','customer','product','temp_margin','temp_margin2','month','year','company','region','emails']

    def get_region(self, sal:SalesRecords2):
        ak=['EAST']
        ag=['WEST']
        an=["NORTH"]
        la=['LAGOS']
        ca=['CONSUMER']
        ba=['BUSINESS','NBMA']
        sta=['STALLION']

        if any(x in sal.temp_region.upper() for x in ak):
            return "EAST"
        if any(x in sal.temp_region.upper() for x in ag):
            return "WEST"
        if any(x in sal.temp_region.upper() for x in an):
            return "NORTH"
        if any(x in sal.temp_region.upper() for x in la):
            return "LAGOS"
        if any(x in sal.temp_region.upper() for x in ca):
            return "CONSUMER"
        if any(x in sal.temp_region.upper() for x in ba):
            return "DISTRIBUTORS",
        if any(x in sal.temp_region.upper() for x in sta):
            return "STALLION"
        else:
            return "OTHERS"
        
    def get_emails(self, acct):
        region = self.get_region(acct)

        # Cache mapping for performance
        if not hasattr(self, "_region_mapping"):
            self._region_mapping = {}
            qs = salesStructure.objects.values("region", "email")
            for row in qs:
                reg = row["region"].upper()
                if reg not in self._region_mapping:
                    self._region_mapping[reg] = []
                self._region_mapping[reg].append(row["email"])

        # Get all emails for region as comma-separated string
        emails = self._region_mapping.get(region.upper(), [])
        return ", ".join(emails) if emails else "no-email@example.com"  

    

    

class AccountsUploadSerializer (serializers.ModelSerializer):
    class Meta:
        model=AccountsUpload
        fields='__all__'

class capacityUploadSerializer (serializers.ModelSerializer):
    class Meta:
        model=capacityUpload
        fields='__all__'