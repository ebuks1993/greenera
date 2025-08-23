from rest_framework import serializers
from django.db import transaction
from django.db.models import Count
from .models import Appcall , rep,customer,Visit , Appcall, Failcalls,areaManager
import requests

from datetime import date , timedelta

class AppcallSerializer (serializers.ModelSerializer):
    class Meta:
        model=Appcall
        fields='__all__'



    
    def save(self, **kwargs):

        ## GET THE DATE
        today=date.today()
        three_days_back = today - timedelta(days=3)





        ## get the data from the app 
        try:
            laprsaco=requests.get(f"https://greenlifepharma.smartsellerafrica.com/api/data/604ae0939314fcf64605056/activities?date_from={today}&date_to={today}")
            laprsaco1=laprsaco.json()
            laprsaco2=laprsaco1['activities']
        except:

            # update the table to failed in the event of an error 
            Appcall.objects.create(callDate=today,Status="failed")
            raise
        


        ## get all the reps inside the information 
        zico=[]
        for i in laprsaco2:
            x={"salesman_id":str(i['salesman_code']),"salesman_name":str(i['fullname'])}
            zico.append(x)
        
        ## get the unique rep name in a json format
        zico1 = []
        seen = set()
        for d in zico:
            t = tuple(sorted(d.items()))
            if t not in seen:
                seen.add(t)
                zico1.append(d)

        ## put the data in a model format for django to understand 
        repsdata=[rep(salesman_id=item['salesman_id'],salesman_name=item['salesman_name']) for item in zico1]

        unique_objs = {obj.salesman_id: obj for obj in repsdata}.values()
        

        ## pass in the bulk data to the database and if it already exist , update it 
        with transaction.atomic():
            rep.objects.bulk_create(
                unique_objs,
                update_conflicts=True,
                unique_fields=['salesman_id'],
                update_fields=['salesman_name']
            )

        #---------------------------------------------------- level 2 ----------------------------------------------------------------------
        ## get all  unique customers in the data 

        wico=[]
        for i in laprsaco2:
            x={"cust_code":str(i['cust_code']),"name":str(i['cust_name']),"cust_location":str(i['cust_location']),"cust_latitude":str(i['cust_latitude'])
            ,"cust_longitude":str(i['cust_longitude']),"cust_channel":str(i['cust_channel']),"rep":str(i['salesman_code'])}
            wico.append(x)
        
        wico1 = []
        seen = set()
        for d in wico:
            t = tuple(sorted(d.items()))
            if t not in seen:
                seen.add(t)
                wico1.append(d)

        # print(wico1)
        ## put the extracted customer  data in a model format for django to understand 
        custdata=[customer(cust_code=item['cust_code'],name=item['name'],cust_location=item['cust_location'],cust_latitude=item['cust_latitude'],
                      cust_longitude=item['cust_longitude'],channel=item['cust_channel'],rep_id=item['rep']) for item in wico1]
        
        unique_objs1 = {obj.cust_code: obj for obj in custdata}.values()

        ## pass in the bulk data to the database and if it already exist , update it 
        with transaction.atomic():
            customer.objects.bulk_create(
                unique_objs1,
                update_conflicts=True,
                unique_fields=['cust_code'],
                update_fields=['name','cust_location','cust_latitude','cust_longitude','channel','rep_id']
            )

       #----------------------------------------------------level 3 ------------------------------------------------- 
        ## bring in the actual visit 
        vico=[]
        for i in laprsaco2:
            x={"a_code":str(i['a_code']),"latitude":str(i['latitude'])
            ,"longitude":str(i['longitude']),"customer":str(i['cust_code']),"rep":str(i['salesman_code']),"contactname":str(i['contactname']),
                "rank_desc":str(i['rank_desc']),"distance":str(i['distance']),"joint_work_descn":str(i['joint_work_descn']),
                "visit_date":str(i['visit_date']),"createdate":str(i['createdate']),
                "activity_product":str(i['activity_product']),"activity_description":str(i['activity_description']),
                "joint_work_desc":str(i['joint_work_descn'])}
            vico.append(x)
        
        ## put the extracted visit  data in a model format for django to understand 
        visitdata=[Visit(a_code=item['a_code'],contactname=item['contactname'],latitude=item['latitude'],
                      longitude=item['longitude'],customer_id=item['customer'],rep_id=item['rep'],rank_desc=item['rank_desc'],
                      distance=item['distance'],joint_work_descn=item['joint_work_descn'],
                       visit_date=item['visit_date'],createdate=item['createdate'],activity_product=item['activity_product'],
                        activity_comment=item['activity_description'] )  for item in vico]

        unique_objs2 = {obj.a_code: obj for obj in visitdata}.values()
        ## pass in the bulk data to the database and if it already exist , update it 
        with transaction.atomic():
            Visit.objects.bulk_create(
                unique_objs2,
                update_conflicts=True,
                unique_fields=['a_code'],
                update_fields=['contactname','latitude','longitude','customer_id','rep_id','rank_desc','distance','joint_work_descn',
                               'visit_date','createdate','activity_product','activity_comment' ]
            )



        #--------------------------- UPDATE THE TRANSACTION TABLE ---------------------------------------------

        Appcall.objects.create(callDate=today,Status="successful")

    
        pass




class MgrSerializer(serializers.ModelSerializer):
    # reps=RepSerializer(many=True, source='areamgrs')
    class Meta:
        model=areaManager
        fields='__all__'

class customerSerializer(serializers.ModelSerializer):
    class Meta:
        model=customer
        fields='__all__'


class visitSerializer(serializers.ModelSerializer):
    customer=serializers.SerializerMethodField()
    rep= serializers.SerializerMethodField()
    areamanager=serializers.SerializerMethodField()
    mails=serializers.SerializerMethodField()

    class Meta:
        model=Visit
        fields=['visit_date','distance','joint_work_descn','customer','rep','areamanager','mails']
        # fields='__all__'



    
    def get_customer(self,visit:Visit):
        return visit.customer.name
    
    def get_rep(self,visit:Visit):
        return visit.rep.salesman_name
    
    def get_areamanager(self,visit:Visit):
        a= visit.rep.areaManager
        if a is None:
            return " "
        else:
            return visit.rep.areaManager.name
    
    def get_mails(self,visit:Visit):
        a=visit.rep.areaManager 
        if a is None :
            a=""
        else: a = visit.rep.areaManager.email


        b=visit.rep.areaManager
        if b is None:
            b=" "
        else:
            b=visit.rep.areaManager.businessManager.email
        
        c=visit.rep.areaManager
        if c is None:
            c=" "
        else:
            c=visit.rep.areaManager.businessManager.regionManager.email
        
        return f"{a},{b},{c}"


class visitcountSerializer(serializers.ModelSerializer):
    # vio=serializers.IntegerField(read_only=True)
    total=serializers.IntegerField(read_only=True)
    class Meta:
        model=Visit
        fields=['visit_date','distance','customer','total']

class RepVisitSerializer(serializers.ModelSerializer):
    visit= serializers.IntegerField(read_only=True)
    date= serializers.DateField(read_only=True)
    # vio=visitcountSerializer(many=True,source='repss')
    class Meta:
        model=rep
        fields=['salesman_id','salesman_name','areaManager','visit','date']


# class HmdRepVisitSerializer(serializers.ModelSerializer):
#     visit= serializers.IntegerField(read_only=True)
#     date= serializers.DateField(read_only=True)
#     asm= serializers.SerializerMethodField(method_name='asmname')
#     # vio=visitcountSerializer(many=True,source='repss')
#     class Meta:
#         model=rep
#         fields=['salesman_id','salesman_name','areaManager','visit','date','asm']

#     def asmname(self,rep:rep):
#         a=rep.areaManager.name
#         if a is None:
#             return ""
#         else:
#             return rep.areaManager.name

class HmdRepVisitSerializer(serializers.ModelSerializer):
    areaManager=serializers.StringRelatedField()
    visit=serializers.SerializerMethodField()
    # vio=visitcountSerializer(many=True,source='repss')
    class Meta:
        model=rep
        fields=['salesman_id','salesman_name','areaManager','visit']

    def get_visit(self,obj):
        # visits= obj.repss.all()
        vis= obj.repss.filter(distance__lte=0.5)
        visits=vis.values("visit_date").annotate(total=Count("customer")).order_by("-visit_date")# --- groupby visitdate 
        return visitcountSerializer(visits,many=True).data



class RepSerializer(serializers.ModelSerializer):

    class Meta:
        model=rep
        fields='__all__'


# --- in the event of a failed upload 
class failSerializer(serializers.ModelSerializer):
    class Meta:
        model=Failcalls
        fields='__all__'

    def save(self, **kwargs):
        dated=self.validated_data["failDate"]
        ## GET THE DATE
        today=dated





        ## get the data from the app 
        try:
            laprsaco=requests.get(f"https://greenlifepharma.smartsellerafrica.com/api/data/604ae0939314fcf64605056/activities?date_from={today}&date_to={today}")
            laprsaco1=laprsaco.json()
            laprsaco2=laprsaco1['activities']
        except:

            # update the table to failed in the event of an error 
            Appcall.objects.create(callDate=today,Status="failed")
            raise
        


        ## get all the reps inside the information 
        zico=[]
        for i in laprsaco2:
            x={"salesman_id":str(i['salesman_code']),"salesman_name":str(i['fullname'])}
            zico.append(x)
        
        ## get the unique rep name in a json format
        zico1 = []
        seen = set()
        for d in zico:
            t = tuple(sorted(d.items()))
            if t not in seen:
                seen.add(t)
                zico1.append(d)

        ## put the data in a model format for django to understand 
        repsdata=[rep(salesman_id=item['salesman_id'],salesman_name=item['salesman_name']) for item in zico1]

        ## pass in the bulk data to the database and if it already exist , update it 
        with transaction.atomic():
            rep.objects.bulk_create(
                repsdata,
                update_conflicts=True,
                unique_fields=['salesman_id'],
                update_fields=['salesman_name']
            )

        #---------------------------------------------------- level 2 ----------------------------------------------------------------------
        ## get all  unique customers in the data 

        wico=[]
        for i in laprsaco2:
            x={"cust_code":str(i['cust_code']),"name":str(i['cust_name']),"cust_location":str(i['cust_location']),"cust_latitude":str(i['cust_latitude'])
            ,"cust_longitude":str(i['cust_longitude']),"cust_channel":str(i['cust_channel']),"rep":str(i['salesman_code'])}
            wico.append(x)
        
        wico1 = []
        seen = set()
        for d in wico:
            t = tuple(sorted(d.items()))
            if t not in seen:
                seen.add(t)
                wico1.append(d)

        # print(wico1)
        ## put the extracted customer  data in a model format for django to understand 
        custdata=[customer(cust_code=item['cust_code'],name=item['name'],cust_location=item['cust_location'],cust_latitude=item['cust_latitude'],
                      cust_longitude=item['cust_longitude'],channel=item['cust_channel'],rep_id=item['rep']) for item in wico1]

        ## pass in the bulk data to the database and if it already exist , update it 
        with transaction.atomic():
            customer.objects.bulk_create(
                custdata,
                update_conflicts=True,
                unique_fields=['cust_code'],
                update_fields=['name','cust_location','cust_latitude','cust_longitude','channel','rep_id']
            )

       #----------------------------------------------------level 3 ------------------------------------------------- 
        ## bring in the actual visit 
        vico=[]
        for i in laprsaco2:
            x={"a_code":str(i['a_code']),"latitude":str(i['latitude'])
            ,"longitude":str(i['longitude']),"customer":str(i['cust_code']),"rep":str(i['salesman_code']),"contactname":str(i['contactname']),
                "rank_desc":str(i['rank_desc']),"distance":str(i['distance']),"joint_work_descn":str(i['joint_work_descn']),
                "visit_date":str(i['visit_date']),"createdate":str(i['createdate']),
                "activity_product":str(i['activity_product']),"activity_description":str(i['activity_description']),
                "joint_work_desc":str(i['joint_work_descn'])}
            vico.append(x)
        
        ## put the extracted visit  data in a model format for django to understand 
        visitdata=[Visit(a_code=item['a_code'],contactname=item['contactname'],latitude=item['latitude'],
                      longitude=item['longitude'],customer_id=item['customer'],rep_id=item['rep'],rank_desc=item['rank_desc'],
                      distance=item['distance'],joint_work_descn=item['joint_work_descn'],
                       visit_date=item['visit_date'],createdate=item['createdate'],activity_product=item['activity_product'],
                        activity_comment=item['activity_description'] )  for item in vico]


        ## pass in the bulk data to the database and if it already exist , update it 
        with transaction.atomic():
            Visit.objects.bulk_create(
                visitdata,
                update_conflicts=True,
                unique_fields=['a_code'],
                update_fields=['contactname','latitude','longitude','customer_id','rep_id','rank_desc','distance','joint_work_descn',
                               'visit_date','createdate','activity_product','activity_comment' ]
            )



        #--------------------------- UPDATE THE TRANSACTION TABLE ---------------------------------------------

        Appcall.objects.create(callDate=today,Status="successful")




        pass
    

