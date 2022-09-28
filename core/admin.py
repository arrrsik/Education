from django.contrib import admin

from django.contrib import admin
from .models import Person, EmergencyService, Incident


class IncidentInline(admin.TabularInline):
    model = Incident
    extra = 1


@admin.register(Person)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'date', 'phone', 'health', 'gender', 'image') #The value of 'list_editable[2]' refers to 'image', which is not contained in 'list_display'.
    list_editable = ('phone', 'health', 'image')
    list_filter = ('gender',)
    search_fields = ('surname',)
    inlines = (
        IncidentInline,
    )


class IncidentAdmin(admin.ModelAdmin):
    list_display = ('date', 'number', 'status', 'call')
    list_editable = ('status', 'call')
    list_filter = ('call', 'status', 'service')
    ordering = ('-date',)


class EmergencyServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone', 'appeal')
    list_editable = ('code', 'phone')
    list_filter = ('code',)


admin.site.register(Incident, IncidentAdmin)
admin.site.register(EmergencyService, EmergencyServiceAdmin)

