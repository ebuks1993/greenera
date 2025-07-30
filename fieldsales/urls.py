from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register('appcall',views.appcallView, basename="appcalls")
router.register('rep',views.repView,basename="reps")
router.register('cust',views.custView,basename="custs")
router.register('visit',views.visitView,basename="visits")
router.register('fail',views.failedView,basename="fails")


urlpatterns = [
    path('',include(router.urls))
]
