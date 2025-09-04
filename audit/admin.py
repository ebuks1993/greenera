# from django.contrib import admin
# from .models import bank_name   ,bank_balance,bank_reconcilation,BankBalanceUplooad,BankReconcilationeUplooad
# from django.utils.translation import gettext_lazy as _
# from datetime import date , timedelta
# from import_export.admin import ImportExportModelAdmin
# from import_export import resources
# from django.db import transaction
# import pandas as pd 



# # admin.site.register(bank_name)
# # admin.site.register(bank_balance)
# # admin.site.register(bank_reconcilation)



# @admin.register(BankBalanceUplooad)
# class bankBalanceAdmin(admin.ModelAdmin):
#     list_display = ['id', 'report_start_date', 'report_end_date', 'uploaded_at', 'file', 'uploaded_by']

#     def save_model(self, request, obj, form, change):
#         file = obj.file
#         infoma = pd.read_excel(file)

#         # Select required columns
#         fulldata = infoma[["BANK", "BANKCLOSINGBALANCE", "TALLYCLOSINGBALANCE"]]

#         # Convert DataFrame rows to model instances
#         afulldata = [
#             bank_balance(
#                 reporting_date=obj.report_end_date,
#                 bank_id=item['BANK'],
#                 Tally_balance=item['TALLYCLOSINGBALANCE'],
#                 Bank_balance=item['BANKCLOSINGBALANCE'],
#                 uploaded_by=request.user
#             ) 
#             for item in fulldata.to_dict(orient="records")
#         ]

#         # Ensure uniqueness based on (bank, reporting_date)
#         unique_objs = {(obj.bank, obj.reporting_date): obj for obj in afulldata}.values()

#         # Bulk insert or update
#         with transaction.atomic():
#             bank_balance.objects.bulk_create(
#                 unique_objs,
#                 update_conflicts=True,
#                 unique_fields=['bank', 'reporting_date'],
#                 update_fields=['Bank_balance', 'Tally_balance', 'uploaded_by']
#             )

#         return super().save_model(request, obj, form, change)




# @admin.register(bank_balance)
# class bankBalanceAdmin(admin.ModelAdmin):
#     list_display=['id','reporting_date','bank','Bank_balance','Tally_balance','uploaded_by']



# # class BankreconcilationResource(resources.ModelResource):
# #     class Meta:
# #         model=bank_reconcilation
# #         fields=['reporting_date','bank','Amount','Remark','Description','appearance']

# @admin.register(BankReconcilationeUplooad)
# class bankBalanceAdmin(admin.ModelAdmin):
#     list_display=['id','report_start_date','report_end_date','uploaded_at','file','uploaded_by']


# @admin.register(bank_reconcilation)
# class bankReconcilationAdmin(admin.ModelAdmin):

#     list_display=['reporting_date','bank','Amount','Remark','Description','appearance','Status',]
#     readonly_fields=['cleared_by','Status','uploaded_by','cleared_on']
#     # search_fields=['Remark']
#     # list_editable=['bank']
#     list_filter=['bank']
    
#     def get_list_display(self, request):
#         if request.user.groups.filter(name="account_bankers").exists():
#             return['bank','Amount','discount']
#         return super().get_list_display(request)
        

#     def discount(self,obj):
#         return 417

#     def get_readonly_fields(self, request, obj = None):
#         if request.user.is_superuser:
#             return []
#         return self.readonly_fields
    


  

#     def get_queryset(self, request):
#         qs= super().get_queryset(request)
#         if request.user.groups.filter(name="account_bankers").exists():
#             return qs.filter(Status="Uncleared")
#         else:
#             return qs
    
#     actions=["mark_as_cleared"]

#     # @admin.action(description=_("Mark selected as cleared"))
#     # def mark_as_cleared( self,request,queryset):
#     #     # updated=queryset.update(bank_reconcilation_Status = "cleared")
#     #     updated=queryset.update(Status = "cleared")
#     #     queryset.update(cleared_by=request.user)
#     #     self.message_user(request,f"{updated} record(s) marked as cleared")

#     @admin.action(description=_("Mark selected as cleared"))
#     def mark_as_cleared( self,request,queryset):
#         today=date.today()
#         if not (request.user.is_superuser or request.user.groups.filter(name="account_bankers").exists()):
#          self.message_user(request, "You do not have permission to run this action.", level="error")
#         else:
#             updated=0
#             for obj in queryset:
#                 obj.Status="cleared"
#                 obj.cleared_by=request.user
#                 obj.cleared_on=today
#                 obj.save(update_fields=['Status','cleared_by','cleared_on'])
#                 bank_balance.objects.filter(id=1).update(Tally_balance=9000)
#                 updated +=1
#             self.message_user(request,f"{updated} records marked as cleared by {request.user}")


    

# @admin.register(bank_name)
# class bankNameAdmin(admin.ModelAdmin):
#     list_display=['id','name','company','uploaded_by']
#     readonly_fields=['uploaded_by']

#     def save_model(self,request,obj,form,change):
#         obj.uploaded_by = request.user
#         super().save_model(request, obj, form, change)

# # Register your models here.
