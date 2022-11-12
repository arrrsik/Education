from django.contrib import admin

from django.contrib import admin
from .models import Person, EmergencyService, Incident


class IncidentInline(admin.TabularInline):
    model = Incident
    extra = 1

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'phone', 'health')
    list_editable = ('phone', 'health')
    readonly_fields = ('phone',)
    list_filter = ('gender',)
    search_fields = ('surname',)
    ordering = ('id',)
    empty_value_display = '-Это текст, который будет отображаться по умолчанию для полей, которые не заданы по умолчанию-'
    inlines = (
        IncidentInline,
    )


class IncidentAdmin(admin.ModelAdmin):
    list_display = ('date', 'number', 'status', 'call')
    list_editable = ('status', 'call')
    readonly_fields = ('call',)
    search_fields = ('status',)
    list_filter = ('call', 'status', 'service')
    ordering = ('-date',)


class EmergencyServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'phone', 'appeal')
    list_editable = ('code', 'phone')
    search_fields = ('code',)
    ordering = ('id',)
    list_filter = ('code',)


admin.site.register(Incident, IncidentAdmin)
admin.site.register(EmergencyService, EmergencyServiceAdmin)

