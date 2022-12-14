from core.forms import PersonForm, IncidentForm, EmergencyServiceForm
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect, reverse
from core.models import Person, EmergencyService, Incident
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.db.models import Avg, Count
from django.views.generic import ListView, CreateView, DetailView, TemplateView, RedirectView, View, UpdateView
from core.filters import *


class BaseView(TemplateView):
    template_name = 'base.html'

'''  Создать представление, отображающее количество всех происшествий. Выводить 404, если их нет.  '''
class IncidentsCountView(ListView):
    model = Incident
    queryset = Incident.objects.all()
    template_name = 'incident/num_of_incident.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incidents'] = get_list_or_404(Incident)
        return context

''' Создать представление, отображающее номер телефона заявителя с определенным id,
        указанным в качестве параметра к запросу. Вернуть 404 если такого заявителя не существует. '''
class PhonePersonView(TemplateView):
    model = Person
    template_name = 'person/num_phone.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = get_object_or_404(Person, pk=self.request.GET.get('pk', 1))
        return context

'''Создать представление, которое перенаправляет пользователя на другую страницу'''
class RedirectPageView(RedirectView):
    pattern_name = 'core:base'

'''Создать представление, которое отображает данные входящего запроса (HttpRequest Attributes)'''
class RequestData(View):

    def get(self, request, *args, **kwargs):
        list_data = [request.scheme, request.body, request.path, request.path_info, request.method]
        return HttpResponse(list_data)

'''Создать представление, которое отображает данные заявителя,
        номер телефона которого передается в параметрах запроса. (querydict)'''
class PersonDateView(TemplateView):
    template_name = 'person/querydict.html'
    context_object_name = 'phone'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phone'] = Person.objects.filter(phone=self.request.GET.get('phone')).first()
        return context

'''Создать представление, отдающее данные заявителя в json-формате. (json response)'''
class JsonView(DetailView):

    def get(self, request, *args, **kwargs):
        return JsonResponse(model_to_dict(Person.objects.get(pk=self.kwargs['pk_slug']), exclude='image'))


class PersonListView(ListView):
    model = Person
    template_name = 'person/person_list.html'
    context_object_name = 'all_persons'

    def get_context_data(self, **kwargs):
        filter = PersonFilter(self.request.GET, queryset=Person.objects.all())
        context = super().get_context_data(**kwargs)
        context['filter'] = filter
        return context


class ServiceListView(ListView):
    model = EmergencyService
    template_name = 'service/service_list.html'
    context_object_name = 'services'


class IncidentListView(ListView):
    model = Incident
    template_name = 'incident/incident.html'
    context_object_name = 'incidents'

    def get_context_data(self, **kwargs):
        filter = IncidentFilter(self.request.GET, queryset=Incident.objects.all())
        context = super().get_context_data(**kwargs)
        context['service_count'] = Incident.objects.annotate(Count('service')).aggregate(Avg('service__count'))['service__count__avg']
        context['filter'] = filter
        return context


class PersonDetailView(DetailView):
    model = Person
    template_name = 'person/person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incidents_person'] = self.object.incidents.all()
        return context


class IncidentDetailView(DetailView):
    model = Incident
    template_name = 'incident/incident_detail.html'
    context_object_name = 'incident'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_incident'] = self.object.applicant
        context['service_incident'] = self.object.service.all()
        return context


class ServiceDetailView(DetailView):
    model = EmergencyService
    template_name = 'service/service_detail.html'
    context_object_name = 'service'


class CreatePersonView(CreateView):
    model = Person
    template_name = "person/create_person.html"
    form_class = PersonForm


class CreateIncidentView(CreateView):
    model = Incident
    template_name = "incident/create_incident.html"
    form_class = IncidentForm


class CreateServiceView(CreateView):
    model = EmergencyService
    template_name = "service/create_service.html"
    form_class = EmergencyServiceForm


class UpdateServiceView(UpdateView):
    model = EmergencyService
    template_name = "service/update_service.html"
    form_class = EmergencyServiceForm


class UpdateIncidentView(UpdateView):
    model = Incident
    template_name = "incident/update_incident.html"
    form_class = IncidentForm


class UpdatePersonView(UpdateView):
    model = Person
    template_name = "person/update_person.html"
    form_class = PersonForm
