# -*- encoding: utf-8 -*-

from rest_framework import serializers
from .models import Magazine, Guide, MagazineDay, DetailGuide


class CountListField(serializers.ListField):
    child = serializers.IntegerField(
        min_value=1,
        max_value=100000,
    )


class ProdListField(serializers.ListField):
    child = serializers.CharField()


class MagazineSerializer(serializers.ModelSerializer):
    """serializador para listar diarios"""
    provider = serializers.CharField(source='provider.name')
    tipo = serializers.SerializerMethodField()
    class Meta:
        model = Magazine
        fields = (
            'pk',
            'name',
            'tipo',
            'provider',
            'description',
        )

    def get_tipo(self,obj):
        return obj.get_tipo_display()


class MagazineDaySerializer(serializers.ModelSerializer):
    """serializador para tabla MagazineDay"""
    magazine = serializers.CharField(source='magazine.name')
    day = serializers.SerializerMethodField()
    class Meta:
        model = MagazineDay
        fields = (
            'pk',
            'magazine',
            'day',
        )

    def get_day(self,obj):
        return obj.get_day_display()


class GuideSerializer(serializers.Serializer):
    """serializador para agregar guias"""
    number = serializers.CharField()
    addressee = serializers.CharField()
    invoce = serializers.CharField(required=False)
    provider = serializers.CharField()
    counts = CountListField()
    prods = ProdListField()
    agente = serializers.CharField()
