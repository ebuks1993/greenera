from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import rep,Appcall,customer,Visit,Failcalls,areaManager
from .serializers import RepSerializer , AppcallSerializer,customerSerializer,visitSerializer,failSerializer, MgrSerializer,RepVisitSerializer,HmdRepVisitSerializer
from django.db.models import Value,F
from django.db.models import Count, Sum, F, Window, Avg, Max, Min 
from django.db.models.functions import TruncDate



class appcallView(ModelViewSet):
    queryset=Appcall.objects.all()
    serializer_class=AppcallSerializer


class repView(ModelViewSet):
    queryset=rep.objects.all()
    serializer_class=RepSerializer


class repVisitView(ModelViewSet):
    def get_queryset(self):
        bam=self.request.query_params.get('mgr')
        if bam:
            query=rep.objects.filter(areaManager_id=int(bam)).filter(repss__distance__lte=0.5).annotate(date=TruncDate('repss__visit_date')).annotate(visit=Count('repss__customer', distinct=True))    
        
        return query
    # queryset=rep.objects.filter(areaManager_id=2).filter(repss__distance__lte=0.5).annotate(date=TruncDate('repss__visit_date')).annotate(visit=Count('repss__customer', distinct=True))
    # queryset=rep.objects.filter(areaManager_id=1)
    serializer_class=RepVisitSerializer

class HmdVisitView(ModelViewSet):
        def get_queryset(self):
            bam=self.request.query_params.get('hmd')
            if bam:
                # query=rep.objects.filter(areaManager_id__businessManager_id=int(bam)).filter(repss__distance__lte=0.5).annotate(date=TruncDate('repss__visit_date')).annotate(visit=Count('repss__customer', distinct=True))
                query=rep.objects.all()    

            return query
        serializer_class=HmdRepVisitSerializer


class visitcountview(ModelViewSet):
    queryset=Visit.objects.annotate(vio=Count('visit_date'))

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
    ).all()
    serializer_class=visitSerializer


class failedView(ModelViewSet):
    queryset = Failcalls.objects.all()
    serializer_class= failSerializer



class mgrViewset(ModelViewSet):
    queryset = areaManager.objects.all()
    serializer_class= MgrSerializer
    
# Create your views here.
