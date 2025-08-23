from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register('appcall',views.appcallView, basename="appcalls")
router.register('rep',views.repView,basename="reps")
router.register('repvisit',views.repVisitView,basename="repvisits")
router.register('cust',views.custView,basename="custs")
router.register('visit',views.visitView,basename="visits")
# router.register('fail',views.failedView,basename="fails")
# router.register('areamanager',views.mgrViewset,basename="areamanagers")
# router.register('hmdvisit',views.HmdVisitView,basename="hmdvisits")



urlpatterns = [
    path('',include(router.urls))
]
