from django.db import models
from fieldsales.models import User



class  sales (models.Model):
    company=(
        ('GREENLIFE','GREENLIFE'),
        ('GREENFALCON','GREENFALCON')
    )
    report_start_date = models.DateField()
    report_end_date = models.DateField()
    uploaded_at = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='sales', max_length=100)
    # uploaded_by = models.CharField( max_length=500)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    company = models.CharField( max_length=500, choices=company,null=True)

class Region(models.Model):
    Name = models.CharField( max_length=500)

class Area (models.Model):
    Name = models.CharField( max_length=500)
    Region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)

class Rep(models.Model):
    Name = models.CharField( max_length=500)
    Area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)

class Group(models.Model):
    Name = models.CharField( max_length=500)
    rep = models.ForeignKey(Rep, on_delete=models.DO_NOTHING)


class Customer(models.Model):
    Name = models.CharField( max_length=500)
    State = models.CharField(max_length=500,null=True)
    Allias = models.CharField( max_length=50,unique=True,primary_key=True)
    Address = models.CharField( max_length=1000,null=True)
    Group = models.ForeignKey(Group, on_delete=models.DO_NOTHING,null=True)

    def __str__(self):
        return self.Name



class Product(models.Model):
    Name = models.CharField( max_length=500,unique=True,primary_key=True)
    Uom = models.CharField( max_length=50)
    QPC = models.DecimalField(max_digits=5, decimal_places=5)
    QPC2 = models.FloatField(null=True)
    rate = models.IntegerField(null=True)
    # price = models.DecimalField( max_digits=5, decimal_places=5,null=True)
    price2 = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.Name


class salesStructure(models.Model):
    region=(
        ('WEST','WEST'),
        ('EAST','EAST'),
        ('LAGOS','LAGOS'),
        ('NORTH','NORTH'),
        ('CONSUMER','CONSUMER'),
        ('OTHERS','OTHERS'),
        ('DISTRIBUTORS','DISTRIBUTORS'),
        ('STALLION','STALLION'))
    
    region =models.CharField(max_length=500, choices=region,null=True)
    email = models.EmailField( max_length=1254)




class SalesRecords(models.Model):
    VoucherNum = models.CharField(max_length=50,)
    # Date = models.DateField( auto_now=False, auto_now_add=False)
    Date = models.CharField(max_length=500,null=True)
    units = models.IntegerField()
    ctns = models.IntegerField()
    rate = models.IntegerField()
    Amount = models.IntegerField()
    temp_region = models.CharField( max_length=500)
    # customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='customers')
    # product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,related_name="products")
    customer = models.CharField(max_length=500)
    product = models.CharField(max_length=500)
    temp_margin = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    temp_margin2 = models.FloatField(null=True)
    month = models.CharField(max_length=50  , null=True)
    year = models.CharField( max_length=50 , null=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['VoucherNum','product'],name="vouchervsproduct")
        ]


class SalesRecords2(models.Model):
    VoucherNum = models.CharField(max_length=50,)
    Date = models.CharField(max_length=500,null=True)
    units = models.IntegerField()
    ctns = models.IntegerField()
    rate = models.IntegerField()
    Amount = models.IntegerField()
    temp_region = models.CharField( max_length=500)
    customer = models.CharField(max_length=500)
    product = models.CharField(max_length=500)
    temp_margin = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    temp_margin2 = models.FloatField(null=True)
    month = models.CharField(max_length=50  , null=True)
    year = models.CharField( max_length=50 , null=True)
    company = models.CharField( max_length=500 , null =True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['VoucherNum','product'],name="vouchervsproduct2")
        ]


# __________________________________________CAPACITY ________________________________________________


class  capacityUpload (models.Model):
    company=(
        ('GREENLIFE','GREENLIFE'),
        ('GREENFALCON','GREENFALCON')
    )
    report_start_date = models.DateField()
    report_end_date = models.DateField()
    uploaded_at = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='capacity', max_length=100)
    # uploaded_by = models.CharField( max_length=500)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    company = models.CharField( max_length=500, choices=company,null=True)


class capacity (models.Model):

    Name = models.CharField( max_length=1000,unique=True)
    Sales = models.FloatField()
    collection = models.FloatField()
    Balance = models.FloatField()
    Allias = models.CharField(max_length=1000,null=True)
    # company = models.CharField( max_length=500, choices=company,null=True)

#____________________________________ACOOUNTS_____________________________________________

class  AccountsUpload (models.Model):
    company=(
        ('GREENLIFE','GREENLIFE'),
        ('GREENFALCON','GREENFALCON')
    )
    report_start_date = models.DateField()
    report_end_date = models.DateField()
    uploaded_at = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='account', max_length=100)
    # uploaded_by = models.CharField( max_length=500)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,blank=True)
    company = models.CharField( max_length=500, choices=company,null=True)


class Accounts (models.Model):

    Name = models.CharField( max_length=1000,unique=True)
    Allias = models.CharField(max_length=1000)
    Parent= models.CharField(max_length=1000)
    Credit_limit = models.FloatField()




    


# Create your models here.
