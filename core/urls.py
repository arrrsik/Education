from django.urls import path, include
from . import views
from project import settings
app_name = 'core'

if settings.CLASS_BASED_VIEWS:

    urlpatterns = [
        path('', views.BaseView.as_view(), name="base"),
        # Создать представление, отображающее количество всех происшествий. Выводить 404, если их нет.
        path('incidents_count/', views.IncidentsCountView.as_view(), name="incidents_count"),#Работает
        # Создать представление, отображающее номер телефона заявителя с определенным id,
        # указанным в качестве параметра к запросу. Вернуть 404 если такого заявителя не существует.
        path('phone_person/', views.PhonePersonView.as_view(), name="phone_person"),#Работает
        #Создать представление, которое перенаправляет пользователя на другую страницу
        path('redirect/', views.RedirectPageView.as_view(), name="redirect"),#Работает
        # Создать представление, которое отображает данные входящего запроса (HttpRequest Attributes)
        path('request_data/', views.RequestData.as_view(), name="request_data"),
        # Создать представление, которое отображает данные заявителя,
        # номер телефона которого передается в параметрах запроса. (querydict)
        path('person_data/', views.PersonDateView.as_view(), name="person_data"),
        # Создать представление, отдающее данные заявителя в json-формате. (json response)
        path('json/<slug:pk_slug>/', views.JsonView.as_view(), name="json"),
        path('list_incident/', views.IncidentListView.as_view(), name='list_incident'),  # Работает
        path('person_list/', views.PersonListView.as_view(), name="person_list"),
        path('service_list/', views.ServiceListView.as_view(), name="service_list"),
        path('person_detail/<int:pk>/', views.PersonDetailView.as_view(), name="person_detail"),
        path('incident_detail/<int:pk>/', views.IncidentDetailView.as_view(), name="incident_detail"),
        path('service_detail/<int:pk>/', views.ServiceDetailView.as_view(), name="service_detail"),
        path('create_person/', views.CreatePersonView.as_view(), name='create_person'),
        path('create_incident/', views.CreateIncidentView.as_view(), name='create_incident'),
        path('create_service/', views.CreateServiceView.as_view(), name='create_service'),
        path('update_person/<int:pk>/', views.UpdatePersonView.as_view(), name='update_person'),
        path('update_incident/<int:pk>/', views.UpdateIncidentView.as_view(), name='update_incident'),
        path('update_service/<int:pk>/', views.UpdateServiceView.as_view(), name='update_service'),
        ]
else:

    urlpatterns = [
        #Базовый шаблон
        path('', views.base, name="base"),
        #Создать представление, отображающее количество всех происшествий. Выводить 404, если их нет.
        path('incidents_count/', views.incidents_count, name='incidents_count'),
        #Создать представление, отображающее номер телефона заявителя с определенным id,
        # указанным в качестве параметра к запросу. Вернуть 404 если такого заявителя не существует.
        path('phone_person/', views.phone_person, name="phone_person"),
        #Создать представление, которое перенаправляет пользователя на другую страницу
        path('redirect/', views.redirect_page, name="redirect"),
        #Создать представление, которое отображает данные входящего запроса (HttpRequest Attributes)
        path('request_data/', views.request_data, name="request_data"),
        #Создать представление, которое отображает данные заявителя,
        #номер телефона которого передается в параметрах запроса. (querydict)
        path('person_data/', views.person_data, name="person_data"),
        #Создать представление, отдающее данные заявителя в json-формате. (json response)
        path('json/<int:pk>/', views.json, name="json"),
        path('person_list/', views.person_list, name="person_list"),
        path('service_list/', views.service_list, name="service_list"),
        path('list_incident/', views.list_incident, name="list_incident"),
        path('person_detail/<int:pk>/', views.person_detail, name="person_detail"),
        path('incident_detail/<int:pk>/', views.incident_detail, name="incident_detail"),
        path('service_detail/<int:pk>/', views.service_detail, name="service_detail"),
        path('create_incident/', views.create_incident, name="create_incident"),
        path('create_person/', views.create_person, name='create_person'),
        path('create_service/', views.create_service, name='create_service'),
        path('update_person/<int:pk>/', views.update_person, name='update_person'),
        path('update_incident/<int:pk>/', views.update_incident, name='update_incident'),
        path('update_service/<int:pk>/', views.update_service, name='update_service'),
        #Фильтрация
        #path('person_filter/', views.person_filter, name='person_filter'),
        #path('incident_filter/', views.incident_filter, name='incident_filter'),
    ]
