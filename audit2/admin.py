from django.contrib import admin
from .models import bank_name   ,bank_balance,bank_reconcilation,BankBalanceUplooad,BankReconcilationeUplooad
from django.utils.translation import gettext_lazy as _
from datetime import date , timedelta
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.db import transaction
import pandas as pd 




@admin.register(bank_name)
class bankNameAdmin(admin.ModelAdmin):
    list_display=['id','name','company','uploaded_by']
    readonly_fields=['uploaded_by']

    def save_model(self,request,obj,form,change):
        obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(BankBalanceUplooad)
class bankBalanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'report_start_date', 'report_end_date', 'uploaded_at', 'file', 'uploaded_by']

    def save_model(self, request, obj, form, change):
        file = obj.file
        infoma = pd.read_excel(file)

        # Select required columns
        fulldata = infoma[["BANK", "BANKCLOSINGBALANCE", "TALLYCLOSINGBALANCE"]]

        # Convert DataFrame rows to model instances
        afulldata = [
            bank_balance(
                reporting_date=obj.report_end_date,
                bank_id=item['BANK'],
                Tally_balance=item['TALLYCLOSINGBALANCE'],
                Bank_balance=item['BANKCLOSINGBALANCE'],
                uploaded_by=request.user
            ) 
            for item in fulldata.to_dict(orient="records")
        ]

        # Ensure uniqueness based on (bank, reporting_date)
        unique_objs = {(obj.bank, obj.reporting_date): obj for obj in afulldata}.values()

        # Bulk insert or update
        with transaction.atomic():
            bank_balance.objects.bulk_create(
                unique_objs,
                update_conflicts=True,
                unique_fields=['bank', 'reporting_date'],
                update_fields=['Bank_balance', 'Tally_balance', 'uploaded_by']
            )

        return super().save_model(request, obj, form, change)
    
@admin.register(bank_balance)
class bankBalanceAdmin(admin.ModelAdmin):
    list_display=['id','reporting_date','bank','Bank_balance','Tally_balance','uploaded_by']

@admin.register(BankReconcilationeUplooad)
class bankBalanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'report_start_date', 'report_end_date', 'uploaded_at', 'file', 'uploaded_by']

    def save_model(self, request, obj, form, change):
        file = obj.file
        infoma = pd.read_excel(file)

        # Select required columns
        fulldata = infoma[["DATE","BANK", "DESCRIPTIONS", "REMARK","AMOUNT","TIMES"]]

        # Convert DataFrame rows to model instances
        afulldata = [
            bank_reconcilation(
                reporting_date=item['DATE'],
                bank_id=item['BANK'],
                Amount=item['AMOUNT'],
                Remark=item['REMARK'],
                Description=item['DESCRIPTIONS'],
                appearance=item['TIMES'],
                end_date=obj.report_end_date,
                uploaded_by=request.user
            ) 
            for item in fulldata.to_dict(orient="records")
        ]

        # Ensure uniqueness based on (bank, reporting_date)
        # unique_objs = {(obj.bank, obj.reporting_date): obj for obj in afulldata}.values()

        # Bulk insert or update
        with transaction.atomic():
            bank_reconcilation.objects.all().delete()

            bank_reconcilation.objects.bulk_create(
                afulldata,
                # update_conflicts=True,
                # unique_fields=['bank', 'end_date'],
                # update_fields=['Bank_balance', 'Tally_balance', 'uploaded_by','reporting_date']
            )

        return super().save_model(request, obj, form, change)
    
@admin.register(bank_reconcilation)
class bankReconcilationAdmin(admin.ModelAdmin):

    list_display=['reporting_date','bank','Amount','Remark','Description','appearance','end_date']
    # readonly_fields=['cleared_by','Status','uploaded_by','cleared_on']
    list_filter=['bank']