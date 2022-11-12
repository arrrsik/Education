from django.urls import path, include
from core.views import views_func, views_class
from project import settings
app_name = 'core'

if settings.CLASS_BASED_VIEWS:
    '''Views Классы'''
    urlpatterns = [
        path('', views_class.BaseView.as_view(), name="base"),
        path('incidents_count/', views_class.IncidentsCountView.as_view(), name="incidents_count"),
        path('phone_person/', views_class.PhonePersonView.as_view(), name="phone_person"),
        path('redirect/', views_class.RedirectPageView.as_view(), name="redirect"),
        path('request_data/', views_class.RequestData.as_view(), name="request_data"),
        path('person_data/', views_class.PersonDateView.as_view(), name="person_data"),
        path('json/<slug:pk_slug>/', views_class.JsonView.as_view(), name="json"),
        path('list_incident/', views_class.IncidentListView.as_view(), name='list_incident'),
        path('person_list/', views_class.PersonListView.as_view(), name="person_list"),
        path('service_list/', views_class.ServiceListView.as_view(), name="service_list"),
        path('person_detail/<int:pk>/', views_class.PersonDetailView.as_view(), name="person_detail"),
        path('incident_detail/<int:pk>/', views_class.IncidentDetailView.as_view(), name="incident_detail"),
        path('service_detail/<int:pk>/', views_class.ServiceDetailView.as_view(), name="service_detail"),
        path('create_person/', views_class.CreatePersonView.as_view(), name='create_person'),
        path('create_incident/', views_class.CreateIncidentView.as_view(), name='create_incident'),
        path('create_service/', views_class.CreateServiceView.as_view(), name='create_service'),
        path('update_person/<int:pk>/', views_class.UpdatePersonView.as_view(), name='update_person'),
        path('update_incident/<int:pk>/', views_class.UpdateIncidentView.as_view(), name='update_incident'),
        path('update_service/<int:pk>/', views_class.UpdateServiceView.as_view(), name='update_service'),
        ]
else:
    '''Views Функции'''
    urlpatterns = [
        path('', views_func.base, name="base"),
        path('incidents_count/', views_func.incidents_count, name='incidents_count'),
        path('phone_person/', views_func.phone_person, name="phone_person"),
        path('redirect/', views_func.redirect_page, name="redirect"),
        path('request_data/', views_func.request_data, name="request_data"),
        path('person_data/', views_func.person_data, name="person_data"),
        path('json/<int:pk>/', views_func.json, name="json"),
        path('person_list/', views_func.person_list, name="person_list"),
        path('service_list/', views_func.service_list, name="service_list"),
        path('list_incident/', views_func.list_incident, name="list_incident"),
        path('person_detail/<int:pk>/', views_func.person_detail, name="person_detail"),
        path('incident_detail/<int:pk>/', views_func.incident_detail, name="incident_detail"),
        path('service_detail/<int:pk>/', views_func.service_detail, name="service_detail"),
        path('create_incident/', views_func.create_incident, name="create_incident"),
        path('create_person/', views_func.create_person, name='create_person'),
        path('create_service/', views_func.create_service, name='create_service'),
        path('update_person/<int:pk>/', views_func.update_person, name='update_person'),
        path('update_incident/<int:pk>/', views_func.update_incident, name='update_incident'),
        path('update_service/<int:pk>/', views_func.update_service, name='update_service'),
    ]
