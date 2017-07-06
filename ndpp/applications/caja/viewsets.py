# -*- encoding: utf-8 -*-
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication
)
from rest_framework.permissions import IsAuthenticated

from datetime import datetime
from django.utils import timezone

from .serializers import (
    PagoSerializer,
)
from .functions import (
    deuda_magazine_agente,
)
from .models import Payment, Invoce


class MovimientosGuideViewSet(viewsets.ModelViewSet):
    """ lista de movimientos de una guia por agente """
    serializer_class = PagoSerializer

    def get_queryset(self):
        guide = self.kwargs['guide']
        return deuda_magazine_agente(guide)
