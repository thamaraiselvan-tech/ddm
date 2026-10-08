"""
Django Admin configuration for Eventify.

Registers models with Django's built-in admin panel for easy database management.
Access at: http://localhost:8000/admin/
"""

from django.contrib import admin
from .models import Event, Participant, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'event_date', 'venue', 'max_seats', 'registered_count', 'seats_left', 'is_active']
    list_filter = ['category', 'is_active', 'event_date']
    search_fields = ['name', 'description', 'venue']
    list_editable = ['is_active']

    def registered_count(self, obj):
        return obj.registered_count
    registered_count.short_description = 'Registered'

    def seats_left(self, obj):
        return obj.seats_left
    seats_left.short_description = 'Seats Left'


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'college', 'created_at']
    search_fields = ['name', 'email', 'college']
    list_filter = ['college']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['participant', 'event', 'registered_at']
    list_filter = ['event', 'registered_at']
    search_fields = ['participant__name', 'event__name']
