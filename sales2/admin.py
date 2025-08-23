from django.contrib import admin
from django.db import transaction
import pandas as pd
from datetime import datetime

from .models import sales,Customer,Product,SalesRecords,capacityUpload,capacity,Accounts,AccountsUpload

# class salesinline(admin.StackedInline):
#         model=SalesRecords
#         extra=2
#         # fields=['report_start_date','report_end_date','uploaded_at','file','uploaded_by','discount']


@admin.register(sales)
class salesAdmin(admin.ModelAdmin):
    list_display=['id','report_start_date','report_end_date','uploaded_at','file','uploaded_by','company']
    readonly_fields=['uploaded_by']
    



    def get_queryset(self, request):
        qs = super().get_queryset(request)
        a=qs.filter(uploaded_by=request.user)
        return a 

    # def discount(self,obj):
    #     return f"{obj.uploaded_by} -- is a good guy"
    
    def save_model(self, request, obj, form, change):
        

        # open the file
        file = obj.file
        # file.open("r")  # ensure it's open
        record=pd.read_excel(file)
        recordz=record.fillna(0)

        ## get the columns that are important 
        record2=recordz[['Voucher Number','Date','Party Name','Party Alias','Item Name','Acutal Quantity','Alternate Actual Quantity','Unit','Purchase Rate','Amount','Purchase/Sales Ledger',"Margin"]]
        record2['Date'] = pd.to_datetime(record2['Date'], dayfirst=True).dt.date
        record2['qpc']=recordz['Acutal Quantity']/recordz['Alternate Actual Quantity']
        



## ________________________________GET THE SALES RECORDS______________________________________

        # susto=record2.groupby(['Item Name','Unit'])[['qpc']].max().reset_index()
        prodsdata=[SalesRecords(VoucherNum=item['Voucher Number'],Date=item['Date'],units=item['Acutal Quantity'],ctns=item['Alternate Actual Quantity'],
                           rate=item['Purchase Rate'],Amount=item['Amount'],temp_region=item['Purchase/Sales Ledger'],customer_id=item['Party Alias'],
                           product_id =item['Item Name'],temp_margin2=item['Margin'],temp_margin=0.00000) for item in record2.to_dict(orient="records")]

        # unique_objs2 = {obj.VoucherNum: obj for obj in prodsdata}.values()
        unique_objs2 = {
            (obj.VoucherNum, obj.product_id): obj for obj in prodsdata
        }.values()


        with transaction.atomic():
            SalesRecords.objects.bulk_create(
                unique_objs2,
                update_conflicts=True,
                unique_fields=['VoucherNum','product'],
                update_fields=['Date','units','ctns','rate','Amount','temp_region','customer','temp_margin2'])
    

        # final write 
        obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)




@admin.register(SalesRecords)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','VoucherNum','Date','units','ctns','rate','Amount','temp_region','customer','product','temp_margin']
# Register your models here.


#_______________________________________________CAPACITY DATA _________________________________________________________________

@admin.register(capacityUpload)
class CapacityUploadAdmin(admin.ModelAdmin):
    list_display=['id','report_start_date','report_end_date','uploaded_at','file','uploaded_by','company']
    readonly_fields=['uploaded_by']

    def save_model(self, request, obj, form, change):
        

        # open the file
        file = obj.file
        # file.open("r")  # ensure it's open
        nrecord=pd.read_excel(file,skiprows=11,skipfooter=1)
        nrecordz=nrecord.fillna(0)
        
        nrecordz.columns=['Name','Sales','collection','balance']
        print(nrecordz.columns)
        # recordz['id']=recordz['name'].str[:5]

        

        fulldata=[capacity(Name=item['Name'],Sales=item['Sales'],collection=item['collection'],Balance=item['balance'],
                               ) for item in nrecordz.to_dict(orient="records")]

        # unique_objs2 = {obj.VoucherNum: obj for obj in prodsdata}.values()
        unique_objs3 = {obj.Name: obj for obj in fulldata}.values()

        with transaction.atomic():
                # clear the table first 
                capacity.objects.all().delete()
                
                capacity.objects.bulk_create(
                unique_objs3,
                update_conflicts=True,
                unique_fields=['Name'],
                update_fields=['collection','Balance'])



        # final write 
        obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(capacity)
class capacityAdmin(admin.ModelAdmin):
     list_display=['Name','Sales','collection','Balance']
     search_fields=['Name']






@admin.register(AccountsUpload)
class AccountsUploadAdmin(admin.ModelAdmin):
    list_display=['id','report_start_date','report_end_date','uploaded_at','file','uploaded_by','company']
    readonly_fields=['uploaded_by']

    def save_model(self, request, obj, form, change):
        

        # open the file
        file = obj.file
        # file.open("r")  # ensure it's open
        Arecord=pd.read_excel(file)
        Arecordz=Arecord.fillna(0)
        
        Arecordz.columns=['Name','Allias','Parent','Credit_limit']
        Arecordz['Allias']= Arecordz['Allias'].astype('int')
        print(Arecordz.columns)

        # recordz['id']=recordz['name'].str[:5]

        Afulldata=[Accounts(Name=item['Name'],Allias=item['Allias'],Parent=item['Parent'],Credit_limit=item['Credit_limit'],
                               ) for item in Arecordz.to_dict(orient="records")]

        # unique_objs2 = {obj.VoucherNum: obj for obj in prodsdata}.values()
        unique_objs3 = {obj.Name: obj for obj in Afulldata}.values()

        with transaction.atomic():
                
                Accounts.objects.bulk_create(
                unique_objs3,
                update_conflicts=True,
                unique_fields=['Name'],
                update_fields=['Allias','Parent','Credit_limit'])
        
        # final write 
        obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)




@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display=['Name','Allias','Parent','Credit_limit']
    search_fields=['Name']

    

    
