from django.contrib import admin

from .models import Appcall , rep,customer,Visit , Appcall,regionManager,areaManager,businessManager    

# Register your models here.


admin.site.register(areaManager)
admin.site.register(regionManager)
admin.site.register(rep)
admin.site.register(Appcall)
admin.site.register(customer)
admin.site.register(businessManager)

