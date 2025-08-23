# from django.contrib import admin
# from django.db import transaction
# import pandas as pd

# from .models import sales,Customer,Product,SalesRecords


# @admin.register(sales)
# class salesAdmin(admin.ModelAdmin):
#     list_display=['id','report_start_date','report_end_date','uploaded_at','file','uploaded_by']
    
#     def save_model(self, request, obj, form, change):
        

#         # open the file
#         file = obj.file
#         # file.open("r")  # ensure it's open
#         record=pd.read_excel(file)
#         recordz=record.head(40)

#         ## get the columns that are important 
#         record2=recordz[['Voucher Number','Date','Party Name','Party Alias','Item Name','Acutal Quantity','Alternate Actual Quantity','Unit','Purchase Rate','Amount','Purchase/Sales Ledger',"Margin"]]
#         record2['qpc']=recordz['Acutal Quantity']/recordz['Alternate Actual Quantity']
        

#         ## GET THE UNIQUE CUSTOMERS 
#         custo=record2.groupby(['Party Alias','Party Name'])[['Acutal Quantity']].sum().reset_index()
#         custsdata=[Customer(Name=item['Party Name'],Allias=item['Party Alias'],State='',Address='',Group=None) for item in custo.to_dict(orient="records")]

#         unique_objs = {obj.Allias: obj for obj in custsdata}.values()


#         with transaction.atomic():
#             Customer.objects.bulk_create(
#                 unique_objs,
#                 update_conflicts=True,
#                 unique_fields=['Allias'],
#                 update_fields=['Name','State','Address','Group']
#             )

# #-------------------------------------------------------------------------------------------------------------------------------

#         ## GET THE UNIQUE PRODUCTS 
#         pusto=record2.groupby(['Item Name','Unit'])[['qpc']].max().reset_index()
#         prodsdata=[Product(Name=item['Item Name'],Uom=item['Unit'],QPC=0.00000,QPC2=item['qpc'],rate=0,price2=0.00) for item in pusto.to_dict(orient="records")]

#         unique_objs1 = {obj.Name: obj for obj in prodsdata}.values()


#         with transaction.atomic():
#             Product.objects.bulk_create(
#                 unique_objs1,
#                 update_conflicts=True,
#                 unique_fields=['Name'],
#                 update_fields=['Uom','QPC','rate','price2']
#             )



# ## ________________________________GET THE SALES RECORDS______________________________________

#         # susto=record2.groupby(['Item Name','Unit'])[['qpc']].max().reset_index()
#         prodsdata=[SalesRecords(VoucherNum=item['Voucher Number'],Date=item['Date'],units=item['Acutal Quantity'],ctns=item['Alternate Actual Quantity'],
#                            rate=item['Purchase Rate'],Amount=item['Amount'],temp_region=item['Purchase/Sales Ledger'],customer_id=item['Party Alias'],
#                            product_id =item['Item Name'],temp_margin2=item['Margin'],temp_margin=0.00000) for item in record2.to_dict(orient="records")]

#         # unique_objs2 = {obj.VoucherNum: obj for obj in prodsdata}.values()
#         # unique_objs2 = {
#         #     (obj.VoucherNum, obj.product_id): obj for obj in prodsdata
#         # }.values()


#         with transaction.atomic():
#             SalesRecords.objects.bulk_create(
#                 prodsdata,
#                 update_conflicts=True,
#                 unique_fields=['id'],
#                 update_fields=['VoucherNum','Date','units','ctns','rate','Amount','temp_region','customer','product','temp_margin2'])
    

#         # final write 
#         super().save_model(request, obj, form, change)





    
# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display=['Allias','Name','State','Address','Group']

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display=['Name','Uom','QPC2','rate','price2']


# @admin.register(SalesRecords)
# class ProductAdmin(admin.ModelAdmin):
#     list_display=['id','VoucherNum','Date','units','ctns','rate','Amount','temp_region','customer','product','temp_margin']
# # Register your models here.
