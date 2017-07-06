# -*- encoding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from datetime import datetime

from applications.miscelanea.models import Provider, Vendor

from .models import (
    Magazine,
    MagazineDay,
    Guide,
    DetailGuide,
    Asignation,
    DetailAsignation
)

from .serializers import (
    MagazineSerializer,
    GuideSerializer,
    MagazineDaySerializer
)


class MagazineListViewSet(viewsets.ModelViewSet):
    """servicio que lista diarios y productos"""
    queryset = Magazine.objects.filter(
        disable=False,
    )
    serializer_class = MagazineSerializer


class MagazineDayViewSet(viewsets.ModelViewSet):
    """servicio que lista magazine_day"""
    queryset = MagazineDay.objects.filter(
        magazine__disable=False,
    )
    serializer_class = MagazineDaySerializer


class GuideAddViewSet(viewsets.ViewSet):
    """servicio que crea una guia"""

    def create(self, request):
        serializado = GuideSerializer(data=request.data)
        if serializado.is_valid():
            #recuperamos datos de Guia
            number = serializado.validated_data['number']
            addressee = serializado.validated_data['addressee']
            number_invoce = serializado.validated_data['invoce']
            proveedor = serializado.validated_data['provider']
            provider = Provider.objects.get(pk=proveedor)
            date = datetime.now()

            if not Guide.objects.filter(number=number,anulate=False).exists():
                guide = Guide(
                    number=number,
                    number_invoce=number_invoce,
                    addressee=addressee,
                    provider=provider,
                    date=date,
                    user_created=self.request.user,
                )
                guide.save()

                #reuperamos datos de MagazinesDay
                counts = serializado.validated_data['counts']
                prods = serializado.validated_data['prods']

                for p,c in zip(prods,counts):
                    magazine_day = MagazineDay.objects.get(
                        pk=p,
                    )
                    guide_detail = DetailGuide(
                        magazine_day=magazine_day,
                        guide=guide,
                        count=c,
                        precio_unitario=magazine_day.precio_venta,
                        precio_tapa=magazine_day.precio_tapa,
                        precio_guia=magazine_day.precio_guia,
                        precio_sunat=magazine_day.precio_guia,
                        user_created=self.request.user,
                    )
                    guide_detail.save()

                    #asignaos a vendedro
                    #recuperamos el agente
                    pk_vendor = serializado.validated_data['agente']
                    vendor = Vendor.objects.get(pk=pk_vendor)
                    #creamos la asignacion
                    asignatio = Asignation(
                        detail_guide=guide_detail,
                        date=datetime.now().date(),
                        user_created=self.request.user,
                    )
                    asignatio.save()
                    #creamos la asignacion detalle
                    detail_asignation = DetailAsignation(
                        vendor=vendor,
                        asignation=asignatio,
                        count=c,
                        precio_venta=guide_detail.precio_unitario,
                        user_created=self.request.user,
                    )
                    detail_asignation.save()
                    #actualizmos asignaicon como asihanda
                    guide_detail.asignado=True
                    guide_detail.save()

                res = {'respuesta':'Guardado Correctamente','id':'0'}
            else:
                res = {'respuesta':'ya existe el numero de guia','id':'1'}
        else:
            print '********************'
            print serializado.errors
            res = {'respuesta':'Verifique Los Datos','id':'1'}
        return Response(res)
