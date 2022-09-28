from django import forms
from django.forms import ModelForm, CheckboxInput, ValidationError
from .models import Person, Incident, EmergencyService
from datetime import date


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('surname', 'name', 'patronymic', 'date', 'phone', 'health', 'gender', 'image')
        widgets = {
            "health": forms.Textarea(attrs={' class': 'form-control'}),
        }

    def clean_phone(self):
        cleaned_data = self.cleaned_data['phone']
        if len(str(cleaned_data)) != 11:
            raise ValidationError('Неккоректный номер телефона')
        else:
            return int(cleaned_data)

    def clean_date(self):
        date_now = self.cleaned_data['date']
        if date_now > date.today():
            raise ValidationError('Неккоректная дата рождения')
        else:
            return date_now


class IncidentForm(ModelForm):
    class Meta:
        model = Incident
        fields = ('service', 'victims', 'call', 'applicant')
        service = EmergencyService.objects.all()
        widgets = {
            service: CheckboxInput()
        }


class EmergencyServiceForm(ModelForm):
    code = forms.IntegerField(label='Код', help_text="01-Пожарная служба, 02-Полиция, 03-Скорая помощь")

    class Meta:
        model = EmergencyService
        fields = ('name', 'phone', 'code')
