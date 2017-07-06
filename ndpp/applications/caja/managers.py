from django.db.models import F, FloatField, Sum, Q, CharField, Max,ExpressionWrapper,Value as V
from django.db.models.functions import Upper,Coalesce

from datetime import datetime

from django.conf import settings
from django.db import models


class PaymentManager(models.Manager):

    #consulta que suma os pagos de una detalle asignacion
    def suma_payment(self, pk_asignation):
        #funcion que devuleve cantidad de diarios cancelados
        suma_total = self.filter(
            detail_asignation__pk=pk_asignation,
            anulate=False,
        ).aggregate(suma=Sum(F('count_payment')+F('count_return')))

        if not suma_total['suma'] == None:
            return suma_total['suma']
        else:
            return 0
