from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models
from .forms import OsobaForm, TelefonForm, EmailForm
from django.http import HttpResponseBadRequest
from .util import search


class Index(ListView):
    model = models.Osoba
    template_name = 'spis_tel/index.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q', '')
        results = search(query)
        data = super().get_context_data(**kwargs)
        data['query'] = query
        data['results'] = results
        return data

class CreateOsoba(CreateView):

    template_name = 'spis_tel/add_person.html'
    fields = ('imie', 'nazwisko')
    model = models.Osoba
    success_url = reverse_lazy('list')

class CreateTelefon(CreateView):

    context_object_name = 'osoba'
    form = TelefonForm
    template_name = 'spis_tel/add_telefon.html'
    fields = ('telefon',)
    model = models.Telefon
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.instance.osoba = models.Osoba.objects.get(id=self.kwargs.get('pk'))
        return super(CreateTelefon, self).form_valid(form)

class CreateEmail(CreateView):
    form = EmailForm
    template_name = 'spis_tel/add_email.html'
    fields = ('email',)
    model = models.Email
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.instance.osoba = models.Osoba.objects.get(id=self.kwargs.get('pk'))
        return super(CreateEmail, self).form_valid(form)

class UpdateOsoba(UpdateView):

    context_object_name = 'osoba'
    template_name = 'spis_tel/update_person.html'
    fields = ('imie', 'nazwisko')
    model = models.Osoba
    success_url = reverse_lazy('list')


class DeleteOsoba(DeleteView):
    template_name = 'spis_tel/delete_person.html'
    model = models.Osoba
    context_object_name = 'osoba_delete'
    success_url = reverse_lazy('list')
    
    def deleteable(_dispatch):
        def decorator(self,request, *args, **kwargs):
            if not models.Telefon.objects.filter(osoba_id=self.kwargs.get('pk')) and not models.Email.objects.filter(osoba_id=self.kwargs.get('pk')):
                return _dispatch(self,request, *args, **kwargs)
            else:
                return HttpResponseBadRequest(content='''ERROR <form action="/"><input type="submit" value="Powrót"/></form>''')
        return decorator

    @deleteable
    def dispatch(self, *args, **kwargs):
        return super(DeleteOsoba, self).dispatch(*args, **kwargs)

