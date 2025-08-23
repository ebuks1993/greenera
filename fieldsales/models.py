from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email=models.EmailField(unique=True)

class regionManager(models.Model):
    name = models.CharField(max_length=500)
    hmd = models.CharField( max_length=500)
    email = models.EmailField( max_length=254)

    def __str__(self):
        return self.name

class businessManager(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField( max_length=254)
    regionManager = models.OneToOneField(regionManager, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class areaManager(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField( max_length=254)
    businessManager = models.ForeignKey(businessManager, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class rep(models.Model):
    salesman_name= models.CharField( max_length=500)
    salesman_id = models.CharField( max_length=50, unique=True , primary_key=True)
    areaManager = models.ForeignKey(areaManager, on_delete=models.DO_NOTHING , null=True , blank=True , related_name="areamgrs")

    def __str__(self):
        return self.salesman_name


class customerCat(models.Model):
    cust_channel= models.CharField( max_length=500, unique=True,primary_key=True)
    name = models.CharField(max_length=500)

class customer(models.Model):
    name = models.CharField( max_length=500)
    cust_code = models.CharField( max_length=500 ,unique=True, primary_key=True)
    cust_location=models.CharField(max_length=5000)
    cust_latitude = models.CharField( max_length=500)
    cust_longitude = models.CharField( max_length=500)
    cust_state = models.CharField(max_length=500,null=True,blank=True)
    cust_channels = models.ForeignKey(customerCat, on_delete=models.DO_NOTHING,null=True,blank=True)
    channel = models.CharField(max_length=500,null=True)
    rep = models.ForeignKey(rep, on_delete=models.DO_NOTHING , related_name="reps")






class Visit(models.Model):
    a_code = models.CharField( max_length=500,unique=True,primary_key=True)
    createdate = models.DateField( auto_now=False, auto_now_add=False,null=True)
    visit_date = models.DateField( auto_now=False, auto_now_add=False,null=True)
    # start_time = models.TimeField( auto_now=False, auto_now_add=False)
    # end_time = models.TimeField( auto_now=False, auto_now_add=False)
    latitude = models.CharField( max_length=500,null=True)
    longitude = models.CharField( max_length=500,null=True)
    activity_product = models.CharField( max_length=500,null=True)
    activity_comment = models.CharField( max_length=5000,null=True)
    contactname = models.CharField( max_length=500,null=True)
    rank_desc = models.CharField( max_length=500,null=True)
    # distance = models.DecimalField( max_digits=5, decimal_places=2,null=True,blank=True)
    distance = models.CharField( max_length=500,null=True)
    joint_work_descn = models.CharField( max_length=500,null=True)
    customer = models.ForeignKey(customer, on_delete=models.DO_NOTHING,null=True)
    rep = models.ForeignKey(rep, on_delete=models.DO_NOTHING,null=True, related_name='repss')





class Appcall(models.Model):
    callDateTrack = models.DateField( auto_now=False, auto_now_add=True)
    callDate = models.DateField()
    Status = models.CharField( max_length=50)


class Failcalls(models.Model):
    failDate=models.DateField()






    

# Create your models here.
