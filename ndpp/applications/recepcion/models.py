# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from model_utils.models import TimeStampedModel

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import models

from applications.miscelanea.models import Provider, Vendor


@python_2_unicode_compatible
class Magazine(TimeStampedModel):
    """tabla para magazine y proucto"""
    MAGAZINE_CHOISES = (
        ('0','Diario'),
        ('1','Producto'),
    )
    name = models.CharField(
        max_length=100
    )
    tipo = models.CharField(
        max_length=2,
        choices=MAGAZINE_CHOISES,
        blank=True,
        null=True,
    )
    provider = models.ForeignKey(Provider)
    description = models.CharField(
        blank=True,
        max_length=100
    )
    disable = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="magazine_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="magazine_modified",
        blank=True,
        null=True,
        editable=False
    )
    afecto = models.BooleanField(default=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class MagazineDay(TimeStampedModel):
    """Producto Dia"""
    DAY_CHOICES = (
        ('0','LUNES'),
        ('1','MARTES'),
        ('2','MIERCOLES'),
        ('3','JUEVES'),
        ('4','VIERNES'),
        ('5','SABADO'),
        ('6','DOMINGO'),
        ('7','LUNES-SABADO'),
    )

    magazine = models.ForeignKey(Magazine)
    day = models.CharField(
        max_length=2,
        choices=DAY_CHOICES
    )
    precio_tapa = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_guia = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="magazineday_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="magazineday_modified",
        blank=True,
        null=True,
        editable=False
    )

    def __str__(self):
        return str(self.magazine.name)+'['+str(self.get_day_display())+']'


@python_2_unicode_compatible
class Guide(TimeStampedModel):
    """Guia de remision"""
    ADDRESSEE_CHOICES = (
        ('0','DPP'),
        ('1','MAX CARGO'),
    )

    number = models.CharField(
        max_length=20,
    )
    date = models.DateField()
    number_invoce = models.CharField(
        blank=True,
        max_length=100
    )
    addressee = models.CharField(
        max_length=2,
        choices=ADDRESSEE_CHOICES
    )
    date_emission = models.DateField(
        blank=True,
        null=True
    )
    provider = models.ForeignKey(Provider)
    date_retunr_cargo = models.DateField(
        blank=True,
        null=True
    )
    plazo_return = models.PositiveIntegerField(default=7)
    anulate = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="guide_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="guide_modified",
        blank=True,
        null=True,
        editable=False
    )
    culmined = models.BooleanField(default=False)
    asignado = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return self.number


@python_2_unicode_compatible
class DetailGuide(TimeStampedModel):
    """guia detalle"""
    magazine_day = models.ForeignKey(MagazineDay)
    guide = models.ForeignKey(Guide)
    count = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_tapa = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_guia = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    precio_sunat = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    discount = models.BooleanField(default=False)
    missing = models.PositiveIntegerField(default=0)
    real_count = models.PositiveIntegerField(default=0)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="detailguide_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="detailguide_modified",
        blank=True,
        null=True,
        editable=False
    )
    anulate = models.BooleanField(default=False)
    culmined = models.BooleanField(default=False)
    asignado = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    en_reparto = models.BooleanField(default=False)

    def __str__(self):
        return str(self.magazine_day)


@python_2_unicode_compatible
class Asignation(TimeStampedModel):
    """salida de Diario"""
    detail_guide = models.ForeignKey(DetailGuide)
    date = models.DateField(auto_now_add=True)
    anulate = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="asignation_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="asignation_modified",
        blank=True,
        null=True,
        editable=False
    )

    def __str__(self):
        return str(self.detail_guide)


@python_2_unicode_compatible
class DetailAsignation(TimeStampedModel):
    """Detalle de una salida"""
    vendor = models.ForeignKey(Vendor)
    asignation = models.ForeignKey(Asignation)
    count = models.PositiveIntegerField()
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="asignationdetail_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="asignationdetail_modified",
        blank=True,
        null=True,
        editable=False
    )
    anulate = models.BooleanField(default=False)
    culmined = models.BooleanField(default=False)

    def __str__(self):
        return str(self.vendor)
