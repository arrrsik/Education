import django_filters as filters
from .models import Incident, Person
from django.db.models import Q, QuerySet


class PersonFilter(filters.FilterSet):
    full_name = filters.CharFilter(label='ФИО', method='filter_full_name')

    class Meta:
        model = Person
        fields = (
            'full_name', 'phone', 'date',
        )

    def filter_full_name(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        for term in value.split():
            return queryset.filter(
                Q(surname__iexact=term) |
                Q(name__iexact=term) |
                Q(patronymic__iexact=term)
            )


class IncidentFilter(filters.FilterSet):
    full_name = filters.CharFilter(label='ФИО', method='filter_full_name')
    code = filters.CharFilter(field_name='service__code', label='Код службы')

    class Meta:
        model = Incident
        fields = (
            'status', 'full_name', 'code'
        )

    def filter_full_name(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        for term in value.split():
            return queryset.filter(
                Q(applicant__surname__iexact=term) |
                Q(applicant__name__iexact=term) |
                Q(applicant__patronymic__iexact=term)
            )
