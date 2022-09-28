from .forms import PersonForm, IncidentForm, EmergencyServiceForm
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect, reverse
from .models import Person, EmergencyService, Incident
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.forms import inlineformset_factory
from django.db.models import Avg, Count
from django.views.generic import ListView, CreateView, DetailView, TemplateView, RedirectView, View, UpdateView
from .filters import *


def base(request): #1
    return render(request, 'base.html')


class BaseView(TemplateView): #2
    template_name = 'base.html'


def incidents_count(request): #3
    incidents = get_list_or_404(Incident)
    return render(request, 'num_of_incident.html',  context={'incidents': incidents})


class IncidentsCountView(ListView): #4
    model = Incident
    queryset = Incident.objects.all()
    template_name = 'num_of_incident.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incidents'] = get_list_or_404(Incident)
        return context


def phone_person(request):#5
    person = get_object_or_404(Person, pk=request.GET.get('pk'))
    return render(request, 'num_phone.html', context={'person': person})


class PhonePersonView(TemplateView): #6
    model = Person
    template_name = 'num_phone.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = get_object_or_404(Person, pk=self.request.GET.get('pk'))
        return context


def redirect_page(request): #7
    return HttpResponseRedirect(reverse('core:base'))


class RedirectPageView(RedirectView):#8
    pattern_name = 'core:base'


def request_data(request): #9
    list_data = [request.scheme, request.body, request.path, request.path_info, request.method]
    return HttpResponse(list_data)


class RequestData(View): #10

    def get(self, request, *args, **kwargs):
        list_data = [request.scheme, request.body, request.path, request.path_info, request.method]
        return HttpResponse(list_data)


def person_data(request): #11
    phone = Person.objects.filter(phone=request.GET.get('phone')).first()
    return render(request, 'querydict.html', context={'phone': phone})


class PersonDateView(TemplateView): #12
    template_name = 'querydict.html'
    context_object_name = 'phone'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phone'] = Person.objects.filter(phone=self.request.GET.get('phone')).first()
        return context


def json(request, pk): #13
    return JsonResponse(model_to_dict(Person.objects.get(pk=pk), exclude='image'))


class JsonView(DetailView): #14

    def get(self, request, *args, **kwargs):
        return JsonResponse(model_to_dict(Person.objects.get(pk=self.kwargs['pk_slug']), exclude='image'))


def person_list(request): #15
    all_persons = Person.objects.all()
    f = PersonFilter(request.GET, queryset=Person.objects.all())
    return render(request, 'person_list.html', context={'all_persons': all_persons, 'filter': f})


class PersonListView(ListView): #16
    model = Person
    template_name = 'person_list.html'
    context_object_name = 'all_persons'


def list_incident(request):#17
    incidents = Incident.objects.all()
    service_count = Incident.objects.annotate(Count('service')).aggregate(Avg('service__count'))['service__count__avg']
    f = IncidentFilter(request.GET, queryset=Incident.objects.all())
    return render(request, 'incident.html', context={'incidents': incidents,
                                                     'service_count': service_count,
                                                     'filter': f})


def service_list(request):
    services = EmergencyService.objects.all()
    return render(request, 'service_list.html', context={'services': services})


class ServiceListView(ListView):
    model = EmergencyService
    template_name = 'service_list.html'
    context_object_name = 'services'


class IncidentListView(ListView):#
    model = Incident
    template_name = 'incident.html'
    context_object_name = 'incidents'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_count'] = Incident.objects.annotate(Count('service')).aggregate(Avg('service__count'))['service__count__avg']
        return context


def person_detail(request, pk):#19
    person = get_object_or_404(Person, pk=pk)
    incidents_person = person.incidents.all()
    return render(request, 'person_detail.html', context={'person': person, 'incidents_person': incidents_person})


class PersonDetailView(DetailView):#20
    model = Person
    template_name = 'person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incidents_person'] = self.object.incidents.all()
        return context


def incident_detail(request, pk):#19
    incident = get_object_or_404(Incident, pk=pk)
    person_incident = Incident.objects.get(pk=pk).applicant
    service_incident = Incident.objects.get(pk=pk).service.all()
    return render(request, 'incident_detail.html', context={'incident': incident, 'person_incident': person_incident,
                                                            'service_incident': service_incident})


class IncidentDetailView(DetailView):#20
    model = Incident
    template_name = 'incident_detail.html'
    context_object_name = 'incident'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_incident'] = self.object.applicant
        context['service_incident'] = self.object.service.all()
        return context


def service_detail(request, pk):#19
    service = get_object_or_404(EmergencyService, pk=pk)
    return render(request, 'service_detail.html', context={'service': service})


class ServiceDetailView(DetailView):#20
    model = EmergencyService
    template_name = 'service_detail.html'
    context_object_name = 'service'


def create_person(request): #21
    form = PersonForm(request.POST or None)
    if form.is_valid() and form.clean_date() and form.clean_phone():
        form.save()
        redirect(reverse('core:base'))
    context = {
        'form': form
    }
    return render(request, 'create_person.html', context)


class CreatePersonView(CreateView):#22
    model = Person
    template_name = "create_person.html"
    form_class = PersonForm


def create_incident(request):#23
    form = IncidentForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, 'create_incident.html', context)


class CreateIncidentView(CreateView): #24
    model = Incident
    template_name = "create_incident.html"
    form_class = IncidentForm


class CreateServiceView(CreateView): #26
    model = EmergencyService
    template_name = "create_service.html"
    form_class = EmergencyServiceForm


def create_service(request): #25
    form = EmergencyServiceForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, 'create_service.html', context)


def update_service(request, pk):
    service = EmergencyService.objects.get(pk=pk)
    form = EmergencyServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        service = form.save(commit=False)
        service.save()
    context = {
        'service': service,
        'form': form
    }
    return render(request, 'update_service.html', context)


def update_incident(request, pk):
    incident = Incident.objects.get(pk=pk)
    form = IncidentForm(request.POST or None, instance=incident)
    if form.is_valid():
        incident = form.save(commit=False)
        incident.save()
    context = {
        'incident': incident,
        'form': form
    }
    return render(request, 'update_incident.html', context)


def update_person(request, pk):
    person = Person.objects.get(pk=pk)
    form = PersonForm(request.POST or None, instance=person)
    if form.is_valid():
        person = form.save(commit=False)
        person.save()
    context = {
        'person': person,
        'form': form
    }
    return render(request, 'update_person.html', context)


class UpdateServiceView(UpdateView): #26
    model = EmergencyService
    template_name = "create_service.html"
    form_class = EmergencyServiceForm


class UpdateIncidentView(CreateView): #24
    model = Incident
    template_name = "create_incident.html"
    form_class = IncidentForm


class UpdatePersonView(CreateView):#22
    model = Person
    template_name = "create_person.html"
    form_class = PersonForm
