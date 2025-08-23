from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from .views import AccountsView,AccountsUploadView,capacityUploadView,capacityView,salesView,SalesRecordsView

router=DefaultRouter()
router.register('Account',AccountsView, basename="Acccounts")
router.register('AccountsUpload',AccountsUploadView, basename="AccountsUploads")
router.register('capacityUpload',capacityUploadView, basename="capacityUploads")
router.register('capacity',capacityView, basename="capacitys")
router.register('sales',salesView, basename="saless")
router.register('SalesRecords',SalesRecordsView, basename="SalesRecordss")






urlpatterns = [
    path('',include(router.urls))
]