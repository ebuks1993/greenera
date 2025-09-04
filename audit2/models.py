from django.db import models

from django.db import models

from fieldsales.models import User





class bank_name(models.Model):
    company=(
        ('GREENLIFE','GREENLIFE'),
        ('GREENFALCON','GREENFALCON')
    )
    name = models.CharField( max_length=50)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name="uploader")
    company = models.CharField( max_length=500, choices=company,null=True)

    def __str__(self):
        return self.name




class bank_balance(models.Model):
    reporting_date = models.DateField()
    uploaded_at = models.DateField(auto_now_add=True)
    # bank = models.CharField(max_length=500)
    bank = models.ForeignKey(bank_name, on_delete=models.DO_NOTHING,null=True)
    Bank_balance = models.FloatField()
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name='writer')
    Tally_balance = models.FloatField()

    class Meta:
        constraints=[models.UniqueConstraint(fields=['bank','reporting_date'], name="oned")]





class bank_reconcilation(models.Model):
    reporting_date = models.DateField()
    uploaded_at = models.DateField(auto_now_add=True)
    bank = models.ForeignKey(bank_name, on_delete=models.DO_NOTHING)
    Amount = models.FloatField(default=0)
    Remark = models.CharField( max_length=500,null=True)
    Description = models.TextField(null=True)
    end_date = models.DateField(null=True)
    # Tally_balance = models.FloatField()
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name="writer2")
    appearance = models.IntegerField(default=1,null=True)
    # Status = models.CharField( max_length=50 , default="Uncleared") 
    # cleared_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True,related_name='clearer')
    # cleared_on = models.DateField(null=True,blank=True)

    # class Meta:
        # constraints=[models.UniqueConstraint(fields=['bank','end_date'], name="onedat")]
    

class  BankBalanceUplooad(models.Model):
    report_start_date = models.DateField()
    report_end_date = models.DateField()
    uploaded_at = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='BankBalance', max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name="baluploader")




class  BankReconcilationeUplooad(models.Model):
    report_start_date = models.DateField()
    report_end_date = models.DateField()
    uploaded_at = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='BankReconcilation', max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="reconuploader")












# Create your models here.

# Create your models here.
