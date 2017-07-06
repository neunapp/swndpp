# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
    View,
)
from .models import (
    Magazine,
    MagazineDay,
    Guide,
    DetailGuide,
)

from .forms import (
    MagazineForm,
    ProductAddForm,
    MagazineUpdateForm,
)


class MagazineListView(TemplateView):
    """vista para listar producto o diario"""
    template_name = 'recepcion/magazine/list.html'


class MagazineCreate(CreateView):
    """vista para crear un diario"""
    form_class = MagazineForm
    success_url = reverse_lazy('recepcion_app:list-magazine')
    template_name = 'recepcion/magazine/add.html'

    def form_valid(self, form):
        print '****************'
        #guardamos magazine y recuperaos objeto
        magazine = form.save(commit=False)
        magazine.user_created = self.request.user

        magazine.tipo = '0'
        magazine.afecto = True
        magazine.save()

        for dia in ['0','1','2','3','4','5']:
            magazine_dia1 = MagazineDay(
                magazine=magazine,
                day=dia,
                precio_tapa=form.cleaned_data['precio_tapa'],
                precio_guia=form.cleaned_data['precio_guia'],
                precio_venta=form.cleaned_data['precio_venta'],
                user_created=self.request.user,
            )
            magazine_dia1.save()

        #registro de producto dia-domingo
        magazine_dia2 = MagazineDay(
            magazine=magazine,
            day='6',
            precio_tapa=form.cleaned_data['precio_tapad'],
            precio_guia=form.cleaned_data['precio_guiad'],
            precio_venta=form.cleaned_data['precio_ventad'],
            user_created=self.request.user,
        )
        magazine_dia2.save()

        return super(MagazineCreate, self).form_valid(form)


class ProductCreate(CreateView):
    """vista para crear un prodcuto"""
    form_class = ProductAddForm
    success_url = reverse_lazy('recepcion_app:list-magazine')
    template_name = 'recepcion/magazine/add_prod.html'

    def form_valid(self, form):
        #guardamos magazine y recuperaos objeto
        magazine = form.save(commit=False)
        magazine.user_created = self.request.user

        magazine.tipo = '1'
        magazine.save()

        #registro de produto lines-sabado
        magazine_dia1 = MagazineDay(
            magazine=magazine,
            day='7',
            precio_tapa=form.cleaned_data['precio_tapa'],
            precio_guia=form.cleaned_data['precio_guia'],
            precio_venta=form.cleaned_data['precio_venta'],
            user_created=self.request.user,
        )
        magazine_dia1.save()

        return super(ProductCreate, self).form_valid(form)


class DaysTemplateView(TemplateView):
    template_name = 'recepcion/magazine/days.html'

    def get_context_data(self, **kwargs):
        context = super(DaysTemplateView, self).get_context_data(**kwargs)
        lista_dias = {
            '0':'LUNES',
            '1':'MARTES',
            '2':'MIERCOLES',
            '3':'JUEVES',
            '4':'VIERNES',
            '5':'SABADO',
            '6':'DOMINGO',
        }
        days = sorted(lista_dias.items(), key=operator.itemgetter(0))
        context['days'] = days
        context['tipo'] = self.kwargs.get('tipo',0)
        context['pk'] = self.kwargs.get('pk',0)
        return context


class GuideRegisterView(TemplateView):
    """vista para registrar guias"""
    template_name = 'recepcion/guide/add.html'
