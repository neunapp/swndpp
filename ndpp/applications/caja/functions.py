# -*- encoding: utf-8 -*-
import operator
from datetime import datetime
from applications.recepcion.models import (
    DetailAsignation,
    Guide,
    DetailGuide,
)
from applications.miscelanea.models import Vendor
from .models import Payment, Invoce


#clase que representa un pago
class Pago():
    guide = ''
    pk_asignation = ''
    diario = ''
    tipo = ''
    canilla = ''
    entregado = 0
    devuelto = 0
    pagar = 0
    deuda = 0
    precio_venta = 0.000
    amount = 0.000
    number_operation = ""
    date_operation = ""
    date = ""


class Diarios():
    diario = ''
    cantidad = 0
    por_vencer = False


#funcion que devuelve la lista de magazine que debe un canillas por guia
def deuda_magazine_agente(cod_guide):
    #recuperamos la guia enviada
    guide = Guide.objects.get(number=cod_guide)
    #recuperamos los darios para la guia
    lista_diarios = DetailAsignation.objects.filter(
        culmined=False,
        asignation__detail_guide__anulate=False,
        asignation__detail_guide__guide__number=cod_guide,
        count__gt=0,
        anulate=False,
    ).order_by('asignation__detail_guide__magazine_day__magazine__tipo')
    #
    #variable resultado final
    resultado = []
    #para cada diarios calculamos la cantidad de deuda
    for ld in lista_diarios:
        #verificamo si producto vencio
        tipo = ld.asignation.detail_guide.magazine_day.magazine.tipo
        detail_guide = ld.asignation.detail_guide

        #cargamos diarios a figurar en caja
        p = Pago()
        #
        p.pk_asignation = ld.pk
        #
        if tipo == '1':
            p.diario = detail_guide.magazine_day.magazine.name
        else:
            p.diario = detail_guide.magazine_day
        #
        p.tipo = detail_guide.magazine_day.magazine.get_tipo_display()
        #
        p.canilla = ld.vendor.name
        #
        p.guide = detail_guide.guide.number
        #
        p.entregado = ld.count - Payment.objects.suma_payment(ld.pk)
        #
        #obtenemos la cantidad que se debe
        p.pagar = p.entregado
        #
        p.precio_venta = detail_guide.precio_unitario
        #
        p.amount = p.precio_venta*p.pagar
        #
        p.date = ld.created.date()

        #agregamos a resultado
        resultado.append(p)

    return resultado
