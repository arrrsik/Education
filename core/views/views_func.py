from core import forms
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from core.models import Person, EmergencyService, Incident
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.db.models import Avg, Count
from core.filters import *


def base(request): #1
    return render(request, 'base.html')


'''Создать представление, отображающее количество всех происшествий. Выводить 404, если их нет.'''
def incidents_count(request): #3
    incidents = get_list_or_404(Incident)
    return render(request, 'incident/num_of_incident.html', context={'incidents': incidents})


'''Создать представление, отображающее номер телефона заявителя с определенным id,
        указанным в качестве параметра к запросу. Вернуть 404 если такого заявителя не существует.'''
def phone_person(request):#5
    try:
        person = get_object_or_404(Person, pk=request.GET.get('pk', 1))
        return render(request, 'person/num_phone.html', context={'person': person})
    except ValueError:
        return HttpResponse('Поле ID не может быть пустым, вернитесь и введите id заявителя')


'''Создать представление, которое перенаправляет пользователя на другую страницу'''
def redirect_page(request): #7
    return HttpResponseRedirect(reverse('core:base'))


'''Создать представление, которое отображает данные входящего запроса (HttpRequest Attributes)'''
def request_data(request): #9
    list_data = [request.scheme, request.body, request.path, request.path_info, request.method]
    return HttpResponse(list_data)


'''Создать представление, которое отображает данные заявителя,
        номер телефона которого передается в параметрах запроса. (querydict)'''
def person_data(request): #11
    try:
        phone = Person.objects.filter(phone=request.GET.get('phone')).first()
        return render(request, 'person/querydict.html', context={'phone': phone})
    except ValueError:
        return HttpResponse('Поле телефона не может быть пустым, вернитесь и введите телефон заявителя')


'''Создать представление, отдающее данные заявителя в json-формате. (json response)'''
def json(request, pk): #13
    return JsonResponse(model_to_dict(Person.objects.get(pk=pk), exclude='image'))


def person_list(request): #15
    all_persons = Person.objects.all()
    f = PersonFilter(request.GET, queryset=Person.objects.all())
    return render(request, 'person/person_list.html', context={'all_persons': all_persons, 'filter': f})


def list_incident(request):#17
    incidents = Incident.objects.all()
    service_count = Incident.objects.annotate(Count('service')).aggregate(Avg('service__count'))['service__count__avg']
    filter = IncidentFilter(request.GET, queryset=Incident.objects.all())
    return render(request, 'incident/incident.html', context={'incidents': incidents,
                                                              'service_count': service_count,
                                                              'filter': filter})


def service_list(request):
    services = EmergencyService.objects.all()
    return render(request, 'service/service_list.html', context={'services': services})


def person_detail(request, pk):#19
    person = get_object_or_404(Person, pk=pk)
    incidents_person = person.incidents.all()
    return render(request, 'person/person_detail.html', context={'person': person, 'incidents_person': incidents_person})


def incident_detail(request, pk):#19
    incident = get_object_or_404(Incident, pk=pk)
    person_incident = Incident.objects.get(pk=pk).applicant
    service_incident = Incident.objects.get(pk=pk).service.all()
    return render(request, 'incident/incident_detail.html', context={'incident': incident, 'person_incident': person_incident,
                                                            'service_incident': service_incident})


def service_detail(request, pk):#19
    service = get_object_or_404(EmergencyService, pk=pk)
    return render(request, 'service/service_detail.html', context={'service': service})


def create_person(request): #21
    form = forms.PersonForm(request.POST or None)
    if form.is_valid() and form.clean_date() and form.clean_phone():
        form.save()
        #redirect(reverse('core:base'))
    context = {
        'form': form
    }
    return render(request, 'person/create_person.html', context)


def create_incident(request):#23
    form = forms.IncidentForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, 'incident/create_incident.html', context)


def create_service(request): #25
    form = forms.EmergencyServiceForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, 'service/create_service.html', context)


def update_service(request, pk):
    service = EmergencyService.objects.get(pk=pk)
    form = forms.EmergencyServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        service = form.save(commit=False)
        service.save()
    context = {
        'service': service,
        'form': form
    }
    return render(request, 'service/update_service.html', context)


def update_incident(request, pk):
    incident = Incident.objects.get(pk=pk)
    form = forms.IncidentForm(request.POST or None, instance=incident)
    if form.is_valid():
        incident = form.save(commit=False)
        incident.save()
    context = {
        'incident': incident,
        'form': form
    }
    return render(request, 'incident/update_incident.html', context)


def update_person(request, pk):
    person = Person.objects.get(pk=pk)
    form = forms.PersonForm(request.POST or None, instance=person)
    if form.is_valid():
        person = form.save(commit=False)
        person.save()
    context = {
        'person': person,
        'form': form
    }
    return render(request, 'person/update_person.html', context)
