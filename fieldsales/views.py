from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import rep,Appcall,customer,Visit,Failcalls
from .serializers import RepSerializer , AppcallSerializer,customerSerializer,visitSerializer,failSerializer


class appcallView(ModelViewSet):
    queryset=Appcall.objects.all()
    serializer_class=AppcallSerializer


class repView(ModelViewSet):
    queryset=rep.objects.all()
    serializer_class=RepSerializer


class custView(ModelViewSet):
    queryset=customer.objects.all()
    serializer_class=customerSerializer


class visitView(ModelViewSet):
    queryset=Visit.objects.select_related(
        'customer',
        'rep',
        'rep__areaManager',
        'rep__areaManager__businessManager',
        'rep__areaManager__businessManager__regionManager'
    )
    serializer_class=visitSerializer


class failedView(ModelViewSet):
    queryset = Failcalls.objects.all()
    serializer_class= failSerializer


# Create your views here.
